from abc import ABCMeta, abstractmethod


class DataProviderInterface():
    __metaclass__ = ABCMeta

    def set_answer(self, answer):
        self.answer = answer

    def get_answer(self):
        return self.answer

    @abstractmethod
    def get_question(self, answer):
        pass

    @abstractmethod
    def get_user(self, answer):
        pass

    @abstractmethod
    def get_skill(self, question):
        pass

    @abstractmethod
    def get_question_type(self, question):
        pass

    @abstractmethod
    def get_user_skill(self, user, skill):
        pass

    @abstractmethod
    def set_user_skill(self, user, skill, value):
        pass

    @abstractmethod
    def get_parent_skill(self, skill):
        pass

    @abstractmethod
    def get_difficulty(self, question):
        pass

    @abstractmethod
    def set_difficulty(self, question, value):
        pass

    @abstractmethod
    def get_solving_time(self, answer):
        pass

    @abstractmethod
    def get_correctness(self, answer):
        pass

    @abstractmethod
    def is_first_attempt(self, answer):
        pass

    @abstractmethod
    def get_first_attempts_count(self, question):
        pass