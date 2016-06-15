from collections import defaultdict
from proso.django.util import cache_pure

from proso.models.prediction import PredictiveModel, predict_simple


class HierarchicalPredictiveModel(PredictiveModel):

    def __init__(self, pfae_good=1.0, pfae_bad=0.5, elo_alpha=0.8, elo_dynamic_alpha=0.05):
        self._pfae_good = pfae_good
        self._pfae_bad = pfae_bad
        self._elo_alpha = elo_alpha
        self._elo_dynamic_alpha = elo_dynamic_alpha

        self._parents = None
        self._children = None

    def prepare_phase(self, environment, user, item, time, **kwargs):
        return self.prepare_phase_more_items(environment, user, [item], time, **kwargs)

    def prepare_phase_more_items(self, environment, user, items, time, **kwargs):
        parents = self._load_parents(environment, items)
        all_items = list(set(items + [i for ps in list(parents.values()) for (i, v) in ps]))
        leaves = [i for i, v in self._get_leaves(items)]
        return {
            'skills': dict(list(zip(
                all_items, environment.read_more_items('skill', items=all_items, user=user, default=0)))),
            'first_answers': dict(list(zip(
                leaves, environment.number_of_first_answers_more_items(items=leaves)))),
            'answer_counts': dict(list(zip(
                all_items, environment.read_more_items('answer_count', user=user, items=all_items, default=0)))),
            'difficulties': dict(list(zip(
                leaves, environment.read_more_items('difficulty', items=leaves, default=0)))),
            'last_times': dict(list(zip(
                leaves, environment.last_answer_time_more_items(items=leaves, user=user)))),
            'parents': parents
        }

    def predict_phase(self, data, user, item, time, **kwargs):
        skill = self._load_skill(item, data)
        leaves = self._get_leaves([item])
        difficulty = sum([data['difficulties'][i] * v for i, v in leaves]) / len(leaves)
        return predict_simple(
            skill - difficulty,
            number_of_options=len(kwargs['options']) if 'options' in kwargs else 0,
            guess=kwargs.get('guess'))[0]

    def predict_phase_more_items(self, data, user, items, time, **kwargs):
        return [self.predict_phase(data, user, i, time, **kwargs) for i in items]

    def update_phase(self, environment, data, prediction, user, item, correct, time, answer_id, **kwargs):
        alpha_fun = lambda n: self._elo_alpha / (1 + self._elo_dynamic_alpha * n)
        if data['last_times'][item] is None:
            difficulty_alpha = alpha_fun(data['first_answers'][item])
            data['difficulties'][item] -= difficulty_alpha * (correct - prediction)
            environment.write('difficulty', data['difficulties'][item], item=item, time=time, answer=answer_id)
        parents_per_level = [
            list(set([i_w[0] for i_w in parents])) for parents in self._iterate_parents_per_level(item, data)]
        parents_per_level = list(zip(list(range(len(parents_per_level))), parents_per_level))
        parents_per_level.reverse()
        update_const = self._pfae_good if correct else self._pfae_bad
        difficulty = data['difficulties'][item]
        for level, parents in parents_per_level:
            for parent in parents:
                parent_prediction = predict_simple(
                    self._load_skill(parent, data) - difficulty,
                    number_of_options=len(kwargs['options']) if 'options' in kwargs else 0,
                    guess=kwargs.get('guess'))[0]
                data['skills'][parent] += alpha_fun(data['answer_counts'][parent]) * update_const * (correct - parent_prediction)
                environment.write('skill', data['skills'][parent], item=parent, user=user, time=time, answer=answer_id)
                data['answer_counts'][parent] += 1
                environment.write('answer_count', data['answer_counts'][parent], item=parent, user=user, time=time, answer=answer_id)

    def _load_parents(self, environment, items):
        self._prepare_structure(environment)
        parents = {}
        while len(items) > 0:
            found = [(i, self._parents[i]) for i in items if i in self._parents]
            new_items = set()
            for i, ps in found:
                new_items = new_items.union([x[0] for x in ps])
                parents[i] = ps
            items = list(new_items)
        return parents

    # @cache_pure TODO
    def _prepare_structure(self, environment):
        if self._parents is not None:
            return self._parents, self._children

        parents = defaultdict(lambda: [])
        children = defaultdict(lambda: [])
        for _, child, parent, value in environment.read_all_with_key('parent'):
            parents[child].append((parent, value))
            children[parent].append((child, value))
        self._parents = dict(parents)
        self._children = dict(children)
        return self._parents, self._children

    def _load_skill(self, item, data):
        skill = 0
        for skill_items in self._iterate_parents_per_level(item, data):
            weights = float(sum([i_w1[1] for i_w1 in skill_items]))
            skill += sum([data['skills'][i_w3[0]] * i_w3[1] / weights for i_w3 in skill_items])
        return skill

    def _iterate_parents_per_level(self, item, data):
        to_find = [(item, 1)]
        while len(to_find) > 0:
            yield to_find
            to_find = [iw for ps in [data['parents'][i_w2[0]] for i_w2 in to_find if i_w2[0] in data['parents']] for iw in ps]

    def _get_leaves(self, items):
        to_explore = [(item, 1) for item in items]
        leaves = defaultdict(lambda:0)
        while len(to_explore) > 0:
            new = []
            for item, v in to_explore:
                if item not in self._children:
                    leaves[item] += v
                else:
                    for child, vc in self._children[item]:
                        new.append((child, vc * v))
            to_explore = new
        return list(leaves.items())


class TasksHierarchicalPredictiveModel(HierarchicalPredictiveModel):
    # @cache_pure TODO
    def _prepare_structure(self, environment):
        """ Remove task items from skill tree """
        if self._parents is not None:
            return self._parents, self._children

        parents, children = super()._prepare_structure(environment)

        not_task_instances = [parent for ps in parents.values() for parent, _ in ps]
        self._task_instances = set(parents.keys()) - set(not_task_instances)

        to_delete = set()
        for task_instance in self._task_instances:
            task, vt = parents[task_instance][0]
            skill, vs = parents[task][0]
            parents[task_instance] = [(skill, vs * vt)]
            if (task, vs) in children[skill]:
                children[skill].remove((task, vs))
            children[skill].append((task_instance, vs * vt))
            to_delete.add(task)
        for task in to_delete:
            del parents[task]
            del children[task]

        self._parents = dict(parents)
        self._children = dict(children)
        return self._parents, self._children

    def _iterate_parents_per_level(self, item, data):
        """ Do not track skills for leafs (task instances) """
        parents = super()._iterate_parents_per_level(item, data)
        if item not in self._task_instances:
            return parents
        return list(parents)[1:]
