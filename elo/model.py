import math

INITIAL_DIFFICULTY = 0
INITIAL_SKILL = 0


class EloModel():
    def __init__(self, data_provider):
        self.data = data_provider

    @staticmethod
    def expected_response(user_skill, difficulty, question_type):
        if question_type == 'c':
            return 1. / (1 + math.exp(difficulty - user_skill))
        if question_type == 't':
            return -(user_skill - difficulty)

    @staticmethod
    def compute_user_skill_delta(response, expected_response, question_type):
        K = 0.7
        delta = 0

        if question_type == 'c':
            delta = K * (response - expected_response)
        if question_type == 't':
            delta = K * (expected_response - response)

        return delta

    @staticmethod
    def compute_difficulty_delta(response, expected_response, first_attempts_count, question_type):
        ALPHA = 1.0
        DYNAMIC_ALPHA = 0.05
        K = ALPHA / (1 + DYNAMIC_ALPHA * (first_attempts_count - 1))
        delta = 0

        if question_type == 'c':
            delta = K * (expected_response - response)  # that is K * ((1 - response) - (1 - expected_response))
        if question_type == 't':
            delta = K * (response - expected_response)

        return delta

    def response(self, answer, question_type):
        if question_type == 'c':
            return 1 * self.data.get_correctness(answer)
        if question_type == 't':
            return math.log(self.data.get_solving_time(answer))

    def get_user_skill(self, user, skill):
        user_skill = self.data.get_user_skill(user, skill)
        if user_skill is None:
            # propagate skill form parent if doesnt exist
            parent_skill = self.data.get_parent_skill(skill)
            if parent_skill is None:
                user_skill = INITIAL_SKILL
            else:
                user_skill = self.get_user_skill(user, parent_skill)
            self.data.set_user_skill(user, skill, user_skill)
            return user_skill
        else:
            return user_skill

    def update(self):
        """
        update model using answer provided by data provider
        """
        answer = self.data.get_answer()

        user = self.data.get_user(answer)
        question = self.data.get_question(answer)
        question_type = self.data.get_question_type(question)
        leaf_skill = self.data.get_skill(question)

        user_leaf_skill = self.get_user_skill(user, leaf_skill)
        difficulty = self.data.get_difficulty(question)
        if difficulty is None:
            difficulty = INITIAL_DIFFICULTY
            self.data.set_difficulty(question, difficulty)

        expected_response = self.expected_response(
            user_skill=user_leaf_skill,
            difficulty=difficulty,
            question_type=question_type
        )
        response = self.response(answer, question_type)

        user_skill_delta = self.compute_user_skill_delta(response, expected_response, question_type)
        self.data.set_user_skill(user, leaf_skill, user_leaf_skill + user_skill_delta)
        self.update_parent_skills(user, self.data.get_parent_skill(leaf_skill), response, difficulty, question_type)

        if self.data.is_first_attempt(answer):
            difficulty_delta = self.compute_difficulty_delta(
                response,
                expected_response,
                self.data.get_first_attempts_count(question),
                question_type
            )
            self.data.set_difficulty(question, difficulty + difficulty_delta)

    def update_parent_skills(self, user, skill, response, difficulty, question_type):
        if skill is None:
            return
        user_skill = self.get_user_skill(user, skill)
        expected_response = self.expected_response(
            user_skill=user_skill,
            difficulty=difficulty,
            question_type=question_type
        )

        user_skill_delta = self.compute_user_skill_delta(response, expected_response, question_type)
        self.data.set_user_skill(user, skill, user_skill + user_skill_delta)
        self.update_parent_skills(user, self.data.get_parent_skill(skill), response, difficulty, question_type)