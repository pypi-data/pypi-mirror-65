import numpy as np
from inferelator.utils import Validator as check
from inferelator import utils
from inferelator.regression import base_regression
from inferelator.distributed.inferelator_mp import MPControl
from sklearn.linear_model import ElasticNetCV
import scipy.stats
import copy

ELASTICNET_PARAMETERS = dict(l1_ratio=[0.5, 0.7, 0.9],
                             eps=0.001,
                             n_alphas=50,
                             alphas=None,
                             fit_intercept=True,
                             normalize=False,
                             precompute='auto',
                             max_iter=1000,
                             tol=0.001,
                             cv=3,
                             copy_X=True,
                             verbose=0,
                             n_jobs=1,
                             positive=False,
                             random_state=99,
                             selection='random')

MIN_COEF = 0.1


def elastic_net(X, Y, params):
    """

    :param X: np.ndarray [K x N]
    :param Y: np.ndarray [1 x N]
    :param params: dict
    :return:
    """
    assert check.argument_type(X, np.ndarray)
    assert check.argument_type(Y, np.ndarray)

    (N, K) = X.shape

    min_coef = params.pop('min_coef', MIN_COEF)

    # Fit the linear model using the elastic net
    model = ElasticNetCV(**params).fit(X, Y)

    # Set coefficients below threshold to 0
    coefs = model.coef_  # Get all model coefficients [K, ]
    coefs[np.abs(coefs) < min_coef] = 0.  # Threshold coefficients
    coef_nonzero = coefs != 0  # Create a boolean array where coefficients are nonzero [K, ]

    # If there are non-zero coefficients, redo the linear regression with them alone
    # And calculate beta_resc
    if coef_nonzero.sum() > 0:
        x = X[:, coef_nonzero]
        utils.make_array_2d(Y)
        betas = base_regression.recalculate_betas_from_selected(x, Y)
        betas_resc = base_regression.predict_error_reduction(x, Y, betas)
        return dict(pp=coef_nonzero,
                    betas=betas,
                    betas_resc=betas_resc)
    else:
        return dict(pp=np.repeat(True, K).tolist(),
                    betas=np.zeros(K),
                    betas_resc=np.zeros(K))


class ElasticNet(base_regression.BaseRegression):
    params = ELASTICNET_PARAMETERS

    def __init__(self, X, Y, random_seed, parameters=None):
        self.random_seed = random_seed
        self.params = copy.copy(self.params)
        self.params["random_state"] = random_seed

        if parameters is not None:
            self.params.update(parameters)

        super(ElasticNet, self).__init__(X, Y)

    def regress(self):
        """
        Execute Elastic Net

        :return: list
            Returns a list of regression results that base_regression's pileup_data can process
        """

        if MPControl.is_dask():
            from inferelator.distributed.dask_functions import elasticnet_regress_dask
            return elasticnet_regress_dask(self.X, self.Y, self.params, self.G, self.genes)

        def regression_maker(j):
            level = 0 if j % 100 == 0 else 2
            utils.Debug.allprint(base_regression.PROGRESS_STR.format(gn=self.genes[j], i=j, total=self.G), level=level)

            data = elastic_net(self.X.values,
                               utils.scale_vector(self.Y.get_gene_data(j, force_dense=True).flatten()),
                               self.params)
            data['ind'] = j
            return data

        return MPControl.map(regression_maker, range(self.G), tell_children=False)


class ElasticNetWorkflow(base_regression.RegressionWorkflow):
    """
    Add elasticnet regression into a workflow object
    """

    elastic_net_parameters = None

    def set_regression_parameters(self, **kwargs):
        """
        Set regression parameters for elastic_net
        """

        if len(kwargs.keys()) > 0:
            self.elastic_net_parameters = kwargs

    def run_bootstrap(self, bootstrap):
        X = self.design.get_bootstrap(bootstrap)
        Y = self.response.get_bootstrap(bootstrap)
        utils.Debug.vprint('Calculating betas using MEN', level=0)
        MPControl.sync_processes("pre-bootstrap")
        return ElasticNet(X, Y, self.random_seed, parameters=self.elastic_net_parameters).run()
