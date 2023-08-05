import json
import boto3

def flatten_json(y):
	out = {}

	def flatten(x, name=''):

		# name comes suffixed with a '_', therefore :-1
		if name[:-1].lower() == 'customparameters':
			out.update({ "cp_" + d['group'] : d['item'] for d in x })
		elif name[:-1].lower() == 'userparameters':
			out.update({ "up_" + d['group'] : d['item'] for d in x })
		elif name[:-1].lower() == 'externaluserids':
			out.update({ "extid_" + d['type'] : d['id'] for d in x })
		elif type(x) is dict:
			for a in x:
				flatten(x[a], name + a + '_')
		elif type(x) is list:
			i = 0
			for a in x:
				flatten(a, name + str(i) + '_')
				i += 1
		else:
			out[str(name[:-1])] = str(x)

	flatten(y)
	return out


def lower_keys(x):

	if isinstance(x, list):
		return [lower_keys(v) for v in x]
	elif isinstance(x, dict):
		return dict((k.lower(), lower_keys(v)) for k,v in x.items())
	else:
		return x