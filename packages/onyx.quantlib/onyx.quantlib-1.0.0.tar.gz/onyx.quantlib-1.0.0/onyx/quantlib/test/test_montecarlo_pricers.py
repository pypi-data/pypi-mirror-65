###############################################################################
#
#   Copyright: (c) 2020 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from ..black_scholes import opt_BS
from ..tree_pricers import opt_BT
from ..montecarlo_pricers import MC_vanilla, MC_american
from ..gbm_functions import GbmPricePaths

import numpy as np
import math
import unittest

# --- conversions to daily for MC paths
to_daily = 1.0 / 255.0

OPT_PARMS = (75.0, 100.0, 0.25, 0.05, 0.03, 60)


###############################################################################
class UnitTest(unittest.TestCase):

    # -------------------------------------------------------------------------
    def test_vanilla_convergence(self):
        # --- seed the random generator to make unittest deterministic
        np.random.seed(37)

        # --- price paths parameters
        spot, strike, vol, rd, rf, n_days = OPT_PARMS

        payoff = lambda s: max(s - strike, 0.0)

        term = n_days*to_daily
        rd_daily = rd*to_daily
        rf_daily = rf*to_daily

        # --- exact value
        bs_prem = opt_BS(
            "C", spot, strike, vol, term, rd, rf, ret_type="P")

        vol_scaled = vol*math.sqrt(to_daily)
        prev_rel_err = None

        for n_sims in (1000, 10000, 100000, 1000000):
            paths = spot*GbmPricePaths(
                vol_scaled, n_days, rd_daily, rf_daily, n_sims, True)

            mc_prem, mc_err = MC_vanilla(paths, payoff, rd, rf, term)

            # --- test that the estimate is always within 2-sigma from the
            #     correct value
            self.assertLess(math.fabs(mc_prem - bs_prem) / mc_err, 2.0)

            rel_err = math.fabs(mc_prem - bs_prem) / bs_prem

            # --- test that the relative error improves increasing the number
            #     of samples
            if prev_rel_err is not None:
                self.assertLess(rel_err, prev_rel_err)

            prev_rel_err = rel_err

    # -------------------------------------------------------------------------
    def test_american_convergence(self):
        # --- seed the random generator to make unittest deterministic
        np.random.seed(37)

        # --- price paths parameters
        spot, strike, vol, rd, rf, n_days = OPT_PARMS

        payoff = lambda s: max(s - strike, 0.0)

        term = n_days*to_daily
        rd_daily = rd*to_daily
        rf_daily = rf*to_daily

        # --- semi-exact value using a tree pricer
        bt_prem = opt_BT(
            "C", spot, strike, vol, term, rd, rf, "AMERICAN", n_steps=4080)

        vol_scaled = vol*math.sqrt(to_daily)
        prev_rel_err = None

        for n_sims in (1000, 10000, 100000):
            paths = spot*GbmPricePaths(
                vol_scaled, n_days, rd_daily, rf_daily, n_sims, False)

            mc_prem, mc_err = MC_american(
                paths, payoff, term, rd, rf,
                basis="poly", opt_type="C", spot=spot, strike=strike, vol=vol)

            # print(
            #     n_sims,
            #     math.fabs(mc_prem - bt_prem) / mc_err,
            #     math.fabs(mc_prem - bt_prem) / bt_prem
            # )

            # --- test that the estimate is always within 3-sigma from the
            #     correct value
            self.assertLess(math.fabs(mc_prem - bt_prem) / mc_err, 3.0)

            rel_err = math.fabs(mc_prem - bt_prem) / bt_prem

            # --- test that the relative error improves increasing the number
            #     of samples
            if prev_rel_err is not None:
                self.assertLess(rel_err, prev_rel_err)

            prev_rel_err = rel_err

    # -------------------------------------------------------------------------
    def test_vanilla(self):
        # --- seed the random generator to make unittest deterministic
        np.random.seed(123)

        # --- price paths parameters
        spot, vol, rd, n_sims = (100.0, 0.25, 0.05, 50000)

        vol_scaled = vol*math.sqrt(to_daily)

        # --- test two scenarios for rf (i.e. smaller and larger than rd)
        for rf in (0.03, 0.07):
            rd_daily = rd*to_daily
            rf_daily = rf*to_daily

            for n_days in (60, 120, 255):
                term = n_days*to_daily
                paths = spot*GbmPricePaths(
                    vol_scaled, n_days, rd_daily, rf_daily, n_sims, True)

                for strike in (75.0, 100, 125):
                    # --- payoff function for a call option
                    payoff = lambda s: max(s - strike, 0.0)

                    mc_prem, _ = MC_vanilla(paths, payoff, rd, rf, term)

                    bs_prem = opt_BS(
                        "C", spot, strike, vol, term, rd, rf, ret_type="P")

                    rel_err = math.fabs(mc_prem - bs_prem) / bs_prem

                    # --- test that the MC estimated premium is within 5% of
                    #     exact value
                    self.assertLessEqual(rel_err, 0.05)

    # -------------------------------------------------------------------------
    def test_american(self):
        # --- seed the random generator to make unittest deterministic
        np.random.seed(145)

        # --- price paths parameters
        spot, vol, rd, n_sims = (100.0, 0.25, 0.05, 50000)

        vol_scaled = vol*math.sqrt(to_daily)

        # --- test two scenarios for rf (i.e. smaller and larger than rd)
        for rf in (0.03, 0.07):
            rd_daily = rd*to_daily
            rf_daily = rf*to_daily

            for n_days in (60, 120, 255):
                term = n_days*to_daily
                paths = spot*GbmPricePaths(
                    vol_scaled, n_days, rd_daily, rf_daily, n_sims, False)

                for strike in (75.0, 100, 125):
                    # --- payoff function for a call option
                    payoff = lambda s: max(s - strike, 0.0)

                    mc_prem, _ = MC_american(
                        paths, payoff, term, rd, rf, basis="poly",
                        opt_type="C", spot=spot, strike=strike, vol=vol)

                    bt_prem = opt_BT(
                        "C", spot, strike, vol,
                        term, rd, rf, "AMERICAN", n_steps=4080)

                    rel_err = math.fabs(mc_prem - bt_prem) / bt_prem

                    # --- test that the MC estimated premium is within 5% of
                    #     the binomial tree estimate.
                    self.assertLessEqual(rel_err, 0.05)


if __name__ == "__main__":
    unittest.main(failfast=True)
