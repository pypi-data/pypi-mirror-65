# Globalframework packages
from globalframework.security.input_stats import TextStats
from globalframework.security.provider import SecurityProvider

class PolicyStrength:

    def __init__(self, policyitems={}):
        self.policy = self.get_policy(policyitems)
        self.result = {}


    def get_policy(self, policyitems={}):
        """
            By default:

            min_length=8,  # min length: 8
            max_length=12  # max length: 12
            letters_uppercase=2,  # need min. 2 uppercase letters
            non_letter=3 characters # (digits, specials, anything)
            special_characters=2,  # need min. 2 special characters
            entropybits=30   need a password that has minimum 30 entropy bits (password complexity)
        """
        if len(policyitems) == 0:
            # default policy if policy is not provided
            try:
                policyitems = SecurityProvider().get_securitypolicy_default()
            except:
                policyitems = {"MinCharacters": 8, "MaxCharacters": 12, "UppercaseLetter": 1,
                           "SpecialCharacters": 1, "NonLetters": 1, "entropy_bits": 30}

        return policyitems


    def perform_test(self, password: str):
        """Perform all the provided tests in the policy list"""
        passwordstats = PasswordStats(password)
        self.policy.update({"strength": "0"})

        for test_type, test_value in self.policy.items():
            method = passwordstats.lookupMethod(test_type)
            if method == None:
                continue
            self.result.update({test_type: method(test_value)})

        return self.result



class PasswordStats:
    def __init__(self, password):
        self.textstats = TextStats(password)

    def lookupMethod(self, command):
        return getattr(self, 'test_' + command, None)


    def test_MinCharacters(self, arg):
        return self.textstats.length >= int(arg)


    def test_MaxCharacters(self, arg):
        return self.textstats.length <= int(arg)


    def test_UppercaseLetter(self, arg):
        return self.textstats.letters_uppercase >= int(arg)


    def test_SpecialCharacters(self, arg):
        return self.textstats.special_characters >= int(arg)


    def test_NonLetters(self, arg):
        return self.textstats.non_letter >= int(arg)


    def test_entropy_bits(self, arg):
        return self.textstats.entropy_bits


    def test_strength(self, arg):
        return self.textstats.strength()
