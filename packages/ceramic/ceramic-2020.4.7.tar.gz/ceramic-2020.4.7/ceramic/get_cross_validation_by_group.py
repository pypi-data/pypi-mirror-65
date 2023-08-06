from sklearn.model_selection import train_test_split, KFold
from pandas import DataFrame


def _get_id_data(data, id_columns):
	new_data = data.copy()
	new_data['_row_'] = range(len(data))

	if id_columns is None:
		new_data['_id_'] = range(len(new_data))
		id_columns = ['_id_']
	ids = new_data[id_columns].drop_duplicates()
	return new_data, id_columns, ids


def get_training_test_split_by_group(data, id_columns, test_ratio, random_state=None):
	new_data, id_columns, ids = _get_id_data(data=data, id_columns=id_columns)
	if not isinstance(ids, DataFrame):
		raise TypeError(f'ids is not DataFrame. It is {type(ids)}')

	id_training, id_test = train_test_split(ids, test_size=test_ratio, random_state=random_state)
	training = id_training.merge(new_data, how='left', on=id_columns)
	test = id_test.merge(new_data, how='left', on=id_columns)
	training_indices = training['_row_']
	test_indices = test['_row_']
	return list(training_indices), list(test_indices)


def get_kfold_by_group(data, id_columns, num_splits=5, random_state=None):
	new_data, id_columns, ids = _get_id_data(data=data, id_columns=id_columns)

	kfold = KFold(n_splits=num_splits, shuffle=True, random_state=random_state)
	folds = [
		{
			'training': list(ids.iloc[training_index].merge(right=new_data, on=id_columns, how='left')['_row_']),
			'test': list(ids.iloc[test_index].merge(right=new_data, on=id_columns, how='left')['_row_'])
		}
		for training_index, test_index in kfold.split(ids)
	]
	return folds


def get_cross_validation_by_group(data, id_columns, num_splits=5, holdout_ratio=0.2, random_state=None):
	if holdout_ratio == 0:
		return {
			'validation': list(range(len(data))), 'holdout': [],
			'folds': get_kfold_by_group(data=data, id_columns=id_columns, num_splits=num_splits, random_state=random_state)
		}

	if num_splits < 2:
		training_index, test_index = get_training_test_split_by_group(data=data, id_columns=id_columns, random_state=random_state)
		return {
			'validation': training_index,
			'holdout': test_index,
			'folds': []
		}

	new_data, id_columns, ids = _get_id_data(data=data, id_columns=id_columns)
	validation_index, holdout_index = get_training_test_split_by_group(
		data=new_data, id_columns=id_columns, test_ratio=holdout_ratio
	)

	validation = new_data.iloc[validation_index][id_columns]
	validation_folds = get_kfold_by_group(data=validation, num_splits=num_splits, random_state=random_state, id_columns=id_columns)

	return {
		'validation': validation_index,
		'holdout': holdout_index,
		'folds': [
			{
				'training': list(
					validation.iloc[fold['training']].merge(right=new_data, how='left', on=id_columns)['_row_']
				),
				'test': list(
					validation.iloc[fold['test']].merge(right=new_data, how='left', on=id_columns)['_row_']
				)
			}
			for fold in validation_folds
		]
	}
