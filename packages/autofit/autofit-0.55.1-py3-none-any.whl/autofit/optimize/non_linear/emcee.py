import logging
import math
import os

import emcee
import numpy as np

from autofit import conf, exc
from autofit.optimize.non_linear.non_linear import NonLinearOptimizer
from autofit.optimize.non_linear.non_linear import Result
from autofit.optimize.non_linear.output import MCMCOutput

logger = logging.getLogger(__name__)


class Emcee(NonLinearOptimizer):
    def __init__(self, paths, sigma=3):
        """
        Class to setup and run a MultiNest lens and output the MultiNest nlo.

        This interfaces with an input model_mapper, which is used for setting up the \
        individual model instances that are passed to each iteration of MultiNest.
        """

        super().__init__(paths)

        self.sigma = sigma

        self.nwalkers = conf.instance.non_linear.get("Emcee", "nwalkers", int)
        self.nsteps = conf.instance.non_linear.get("Emcee", "nsteps", int)
        self.check_auto_correlation = conf.instance.non_linear.get(
            "Emcee", "check_auto_correlation", bool
        )
        self.auto_correlation_check_size = conf.instance.non_linear.get(
            "Emcee", "auto_correlation_check_size", int
        )
        self.auto_correlation_required_length = conf.instance.non_linear.get(
            "Emcee", "auto_correlation_required_length", int
        )
        self.auto_correlation_change_threshold = conf.instance.non_linear.get(
            "Emcee", "auto_correlation_change_threshold", float
        )

        logger.debug("Creating Emcee NLO")

    def copy_with_name_extension(self, extension, remove_phase_tag=False):
        copy = super().copy_with_name_extension(
            extension=extension, remove_phase_tag=remove_phase_tag
        )
        copy.sigma = self.sigma
        return copy

    class Fitness(NonLinearOptimizer.Fitness):
        def __init__(self, paths, analysis, instance_from_vector, output_results):
            super().__init__(paths, analysis, output_results)
            self.instance_from_vector = instance_from_vector
            self.accepted_samples = 0

        def fit_instance(self, instance):
            likelihood = self.analysis.fit(instance)

            if likelihood > self.max_likelihood:

                self.max_likelihood = likelihood
                self.result = Result(instance, likelihood)

                if self.should_visualize():
                    self.analysis.visualize(instance, during_analysis=True)

                if self.should_backup():
                    self.paths.backup()

                if self.should_output_model_results():
                    self.output_results(during_analysis=True)

            return likelihood

        def __call__(self, params):

            try:

                instance = self.instance_from_vector(params)
                likelihood = self.fit_instance(instance)

            except exc.FitException:

                likelihood = -np.inf

            return likelihood

    def fit(self, analysis, model):

        output = EmceeOutput(
            model=model,
            paths=self.paths,
            auto_correlation_check_size=self.auto_correlation_check_size,
            auto_correlation_required_length=self.auto_correlation_required_length,
            auto_correlation_change_threshold=self.auto_correlation_change_threshold,
        )

        fitness_function = Emcee.Fitness(
            paths=self.paths,
            analysis=analysis,
            instance_from_vector=model.instance_from_vector,
            output_results=output.output_results,
        )

        emcee_sampler = emcee.EnsembleSampler(
            nwalkers=self.nwalkers,
            ndim=model.prior_count,
            log_prob_fn=fitness_function.__call__,
            backend=emcee.backends.HDFBackend(filename=self.paths.path + "/emcee.hdf"),
        )

        output.save_model_info()

        try:
            emcee_state = emcee_sampler.get_last_sample()
            previuos_run_converged = output.converged

        except AttributeError:

            emcee_state = np.zeros(shape=(emcee_sampler.nwalkers, emcee_sampler.ndim))

            for walker_index in range(emcee_sampler.nwalkers):
                emcee_state[walker_index, :] = np.asarray(
                    model.random_vector_from_priors
                )

            previuos_run_converged = False

        logger.info("Running Emcee Sampling...")

        if self.nsteps - emcee_sampler.iteration > 0 and not previuos_run_converged:

            for sample in emcee_sampler.sample(
                initial_state=emcee_state,
                iterations=self.nsteps - emcee_sampler.iteration,
                progress=True,
                skip_initial_state_check=True,
                store=True,
            ):

                if emcee_sampler.iteration % self.auto_correlation_check_size:
                    continue

                if output.converged and self.check_auto_correlation:
                    break

        logger.info("Emcee complete")

        # TODO: Some of the results below use the backup_path, which isnt updated until the end if thiss function is
        # TODO: not located here. Do we need to rely just ono the optimizer foldeR? This is a good idea if we always
        # TODO: have a valid sym-link( e.g. even for aggregator use).

        self.paths.backup()

        instance = output.most_likely_instance

        analysis.visualize(instance=instance, during_analysis=False)
        output.output_results(during_analysis=False)
        output.output_pdf_plots()
        result = Result(
            instance=instance,
            likelihood=output.maximum_log_likelihood,
            output=output,
            previous_model=model,
            gaussian_tuples=output.gaussian_priors_at_sigma(self.sigma),
        )
        self.paths.backup_zip_remove()
        return result

    def output_from_model(self, model, paths):
        return EmceeOutput(model=model, paths=paths)


class EmceeOutput(MCMCOutput):
    def __init__(
        self,
        model,
        paths,
        auto_correlation_check_size,
        auto_correlation_required_length,
        auto_correlation_change_threshold,
    ):

        super(EmceeOutput, self).__init__(model=model, paths=paths)

        self.auto_correlation_check_size = auto_correlation_check_size
        self.auto_correlation_required_length = auto_correlation_required_length
        self.auto_correlation_change_threshold = auto_correlation_change_threshold

    @property
    def backend(self):
        if os.path.isfile(self.paths.sym_path + "/emcee.hdf"):
            return emcee.backends.HDFBackend(
                filename=self.paths.sym_path + "/emcee.hdf"
            )
        else:
            raise FileNotFoundError(
                "The file emcee.hdf does not exist at the path " + self.paths.path
            )

    @property
    def pdf(self):
        import getdist

        return getdist.mcsamples.MCSamples(samples=self.samples_after_burn_in)

    @property
    def pdf_converged(self):
        return True

    @property
    def samples_after_burn_in(self):

        discard = int(3.0 * np.max(self.auto_correlation_times_of_parameters))
        thin = int(np.max(self.auto_correlation_times_of_parameters) / 2.0)
        return self.backend.get_chain(discard=discard, thin=thin, flat=True)

    @property
    def auto_correlation_times_of_parameters(self):
        return self.backend.get_autocorr_time(tol=0)

    @property
    def previous_auto_correlation_times_of_parameters(self):
        return emcee.autocorr.integrated_time(
            x=self.backend.get_chain()[: -self.auto_correlation_check_size, :, :], tol=0
        )

    @property
    def relative_auto_correlation_times(self):
        return (
            np.abs(
                self.previous_auto_correlation_times_of_parameters
                - self.auto_correlation_times_of_parameters
            )
            / self.auto_correlation_times_of_parameters
        )

    @property
    def converged(self):
        converged = np.all(
            self.auto_correlation_times_of_parameters
            * self.auto_correlation_required_length
            < self.total_samples
        )
        if converged:
            try:
                converged &= np.all(
                    self.relative_auto_correlation_times
                    < self.auto_correlation_change_threshold
                )
            except IndexError:
                return False
        return converged

    @property
    def total_samples(self):
        return len(self.backend.get_chain(flat=True))

    @property
    def total_walkers(self):
        return len(self.backend.get_chain()[0, :, 0])

    @property
    def total_steps(self):
        return len(self.backend.get_log_prob())

    @property
    def most_likely_index(self):
        return np.argmax(self.backend.get_log_prob(flat=True))

    @property
    def most_probable_vector(self):
        """
        Read the most probable or most likely model values from the 'obj_summary.txt' file which nlo from a \
        multinest lens.

        This file stores the parameters of the most probable model in the first half of entries and the most likely
        model in the second half of entries. The offset parameter is used to start at the desired model.

        """
        samples = self.samples_after_burn_in
        return [
            float(np.percentile(samples[:, i], [50]))
            for i in range(self.model.prior_count)
        ]

    @property
    def most_likely_vector(self):
        """
        Read the most probable or most likely model values from the 'obj_summary.txt' file which nlo from a \
        multinest lens.

        This file stores the parameters of the most probable model in the first half of entries and the most likely
        model in the second half of entries. The offset parameter is used to start at the desired model.
        """
        return self.backend.get_chain(flat=True)[self.most_likely_index]

    @property
    def maximum_log_likelihood(self):
        return self.backend.get_log_prob(flat=True)[self.most_likely_index]

    def vector_at_sigma(self, sigma):

        limit = math.erf(0.5 * sigma * math.sqrt(2))

        samples = self.samples_after_burn_in

        return [
            tuple(np.percentile(samples[:, i], [100.0 * (1.0 - limit), 100.0 * limit]))
            for i in range(self.model.prior_count)
        ]

    def vector_from_sample_index(self, sample_index):
        """From a sample return the model parameters.

        Parameters
        -----------
        sample_index : int
            The sample index of the weighted sample to return.
        """
        return list(self.pdf.samples[sample_index])

    def weight_from_sample_index(self, sample_index):
        """From a sample return the sample weight.

        Parameters
        -----------
        sample_index : int
            The sample index of the weighted sample to return.
        """
        return self.pdf.weights[sample_index]

    def likelihood_from_sample_index(self, sample_index):
        """From a sample return the likelihood.

        NOTE: GetDist reads the log likelihood from the weighted_sample.txt file (column 2), which are defined as \
        -2.0*likelihood. This routine converts these back to likelihood.

        Parameters
        -----------
        sample_index : int
            The sample index of the weighted sample to return.
        """
        return self.backend.get_log_prob(flat=True)[sample_index]

    def output_pdf_plots(self):

        pass
