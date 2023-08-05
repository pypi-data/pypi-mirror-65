import warnings
from copy import deepcopy


def validate_fold(model_fold, shared_memory, evaluation_function):
	"""
	:type model_fold: dict
	:type shared_memory: dict
	:type evaluation_function: callable
	:rtype: DataFrame
	"""
	shared_memory['progress_bar'].show(amount=shared_memory['progress_amount'], text='validating ...')
	with warnings.catch_warnings():
		warnings.simplefilter('ignore')

		this_model = deepcopy(model_fold['model'])
		fold = model_fold['fold']
		fold_num = model_fold['fold_num']
		model_name = model_fold['model_name']
		try:
			this_model.fit(X=fold.training.X, y=fold.training.y)
		except Exception as e:
			print(list(fold.training.y)[0:10])
			print(fold.training.y.dtype)
			print('\n'*10)
			print(fold.data.head())

			raise e
		training_evaluation = evaluation_function(this_model.predict(fold.training.X), fold.training.y)
		test_evaluation = evaluation_function(this_model.predict(fold.test.X), fold.test.y)
	shared_memory['progress_amount'] += 1
	return {
		'model': this_model,
		'model_name': model_name,
		'fold_num': fold_num,
		'training_evaluation': training_evaluation,
		'test_evaluation': test_evaluation
	}