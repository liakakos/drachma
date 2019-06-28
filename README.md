[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/liakakos/drachma/blob/master/LICENSE)

# Drachma: DAML Library + Python App for Dwolla Integration

Welcome to Drachma! [Drachma](https://en.wikipedia.org/wiki/Greek_drachma) is a set of [DAML](https://daml.com/) Modules for interfacing between the [Dwolla](https://www.dwolla.com/) payment platform and the DAML Ledger. It also includes a reference application which drives the DAML Templates. The App is implemented in Python using rich Ledger API bindings by [dazl](https://pypi.org/project/dazl/) for interaction with the DAML Ledger

## The DAML Dwolla Library

The [DAML Dwolla Library](https://github.com/liakakos/drachma/tree/master/src/daml/Dwolla) assumes a single operator party and multiple user parties.
The library is organized in a set of modules with distinct functionality. More specifically:

### Onboarding

The Onboarding module is used for bootstrapping the DAML Ledger. The party which assumes the operator role creates an instance of the `Operator` template and invites users by exercising the `Operator_InviteUser` choice. The `UserInvitation` contract is accepted by the user party through the `UserInvitation_Accept` choice and the `User` role contract is created. The user can now start sending requests to the operator.

### Customers


### FundingSources


### Transfers


### Utils



## Getting Started

### 1. Environment

To run Drachma, the DAML SDK must be installed on your system. Click [here](https://docs.daml.com/getting-started/installation.html) for the official installation instructions.


### 2. Clone this repository

```
git clone git@github.com:liakakos/drachma.git
cd drachma
```

## Disclaimer

As the [License](https://github.com/liakakos/drachma/blob/master/LICENSE#L153) states I assume no liability for any damages or losses arising from the use of this Work. Please proceed at your own risk!
