/*
 * Deep Learning Studio - GUI platform for designing Deep Learning AI without programming
 *
 * Copyright (C) 2016-2018 Deep Cognition Inc.
 *
 * All rights reserved.
 */

import { ContainerModule } from 'inversify';
import { BackendApplicationContribution } from '@theia/core/lib/node';
import { AuthBackendContribution } from './auth-backend-contribution';

export default new ContainerModule(bind => {
    bind(BackendApplicationContribution).to(AuthBackendContribution);
});
