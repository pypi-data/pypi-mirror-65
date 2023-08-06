import scipy.special as sf
import numpy as np

from popsynth.distribution import LuminosityDistribution


class SchechterDistribution(LuminosityDistribution):
    def __init__(self, Lmin, alpha, seed=1234, name="shechter"):
        """
        A Schechter luminosity function

        :param Lmin: the minimum luminosity
        :param alpha: the power law index
        :param r_max: the maximum distance to integrate
        :param seed: the random number seed
        :param name: the name
        :returns: None
        :rtype:

        """

        truth = dict(Lmin=Lmin, alpha=alpha)

        super(SchechterDistribution, self).__init__(name=name, seed=seed, truth=truth)

        self._construct_distribution_params(Lmin=Lmin, alpha=alpha)

        self._lf_form = r"\frac{1}{L_{\rm min}^{1+\alpha} \Gamma\left(1+\alpha\right)} L^{\alpha} \exp\left[ - \frac{L}{L_{\rm min}}\right]"

    def phi(self, L):
        """FIXME! briefly describe function

        :param L:
        :returns:
        :rtype:

        """

        return (
            L ** self.alpha
            * np.exp(-L / self.Lmin)
            / (self.Lmin ** (1 + self.alpha) * sf.gamma(1 + self.alpha))
        )

    def draw_luminosity(self, size=1):
        """FIXME! briefly describe function

        :param size:
        :returns:
        :rtype:

        """

        xs = 1 - np.random.uniform(size=size)
        return self.Lmin * sf.gammaincinv(1 + self.alpha, xs)

    def __get_Lmin(self):
        """Calculates the 'Lmin' property."""
        return self._params["Lmin"]

    def ___get_Lmin(self):
        """Indirect accessor for 'Lmin' property."""
        return self.__get_Lmin()

    def __set_Lmin(self, Lmin):
        """Sets the 'Lmin' property."""
        self.set_distribution_params(alpha=self.alpha, Lmin=Lmin)

    def ___set_Lmin(self, Lmin):
        """Indirect setter for 'Lmin' property."""
        self.__set_Lmin(Lmin)

    Lmin = property(___get_Lmin, ___set_Lmin, doc="""Gets or sets the Lmin.""")

    def __get_alpha(self):
        """Calculates the 'alpha' property."""
        return self._params["alpha"]

    def ___get_alpha(self):
        """Indirect accessor for 'alpha' property."""
        return self.__get_alpha()

    def __set_alpha(self, alpha):
        """Sets the 'alpha' property."""
        self.set_distribution_params(alpha=alpha, Lmin=self.Lmin)

    def ___set_alpha(self, alpha):
        """Indirect setter for 'alpha' property."""
        self.__set_alpha(alpha)

    alpha = property(___get_alpha, ___set_alpha, doc="""Gets or sets the alpha.""")
