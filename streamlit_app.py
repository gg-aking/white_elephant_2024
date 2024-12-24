import re

from typing import Union

import streamlit as st


class QA:
	def __init__(self, 
				question_index : int,
				question : str,
				answer_regex : Union[list[str], str],
				match_all : bool = False):
		self._question_index = question_index
		self._question = question
		if isinstance(answer_regex, str):
			answer_regex = [answer_regex]
		self._answer_regex = answer_regex
		self.match_all = match_all

	@property
	def question_index(self):
		return self._question_index

	@property
	def question(self):
		return self._question
	
	@property
	def answer_regex(self):
		return self._answer_regex

	def matches_answer(self, guess : str):
		if self.match_all:
			return all([re.search(r, guess, flags = re.IGNORECASE) for r in self.answer_regex])
		else:
			return any([re.search(r, guess, flags = re.IGNORECASE) for r in self.answer_regex])



questions = dict((i, qa) for i, qa in enumerate([
			QA(0,
				"What are the three gifts brought to Mary at the birth of Jesus?",
				["frankincense", "myrrh", "gold"],
				match_all = True),
			QA(1,
				"What is the theological name for the conception of Christ?",
				["mirac.*concepti", "miracle"]),
			QA(2,
				"According to the canon of the Armenian Apostolic Church, who first converted the King of Armenia to Christianity?",
				["saint.*(grigor|gregory)", "(grigor|gregory).*(illuminat|lusavor)", ]),
			QA(3,
				"What was the name of the inventor of the Armenian Alphabet and what year did s/he create it?",
				["[Մմ]եսրոպ [Մմ]աշտոց|mesrr?o[pb]", "405"],
				match_all = True),
			QA(4,
				"According to the eldest son of Denethor, the Steward of Gondor, what may one not do to enter the volcanic land of the east?",
				["walk|stroll"])
			QA(5,
				"What are the three kinds of cheese used in the making of the world's best boreg?",
				["mozz?arella", "feta", "farmer|californi|fresh"],
				match_all = True),
			QA(6,
				"What job did Sona Tanteeg have in Lebanon?",
				["architect"]),
			QA(7,
				"To what restaurant did Zaroug demand her father take her before/after Sunday barbecues as a child? (multiple possible answers)",
				["panda express", "taco llama", r"in(\-n\-| and | ?& ?)out"]),
			QA(8,
				"Who is Syra's best friend at school?",
				["maya"]),
			QA(9,
				"Who is the most beautiful, hardest working and most loving mother, wife and daughter who also played bass in a high school band called \"17+\"?",
				["zaroug"]),
			]))

if 'q_idx' not in st.session_state:
	st.session_state['q_idx'] = 0

st.header('White Elephant 2024 Quiz')
st.markdown("""8 out of 10 required to gain the password to unlock this year's most interesting present.
	""")
guesses = {}
for q_idx, qa in sorted(questions.items(), key = lambda x : x[0]):
	st.write(f'{q_idx + 1}. {qa.question}')
	guesses[q_idx] = st.text_input(label = '', key = f'q_{q_idx}')

if st.button('Submit'):
	nb_right = 0
	for guess_idx, guess in sorted(guesses.items(), key = lambda x : x[0]):
		qa = questions[guess_idx]
		if qa.matches_answer(guess):
			nb_right += 1
	st.write(f'Number correct: {nb_right}')

