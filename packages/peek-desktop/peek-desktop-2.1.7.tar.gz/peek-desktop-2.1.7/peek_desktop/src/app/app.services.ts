import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";
import {VortexService, VortexStatusService} from "@synerty/vortexjs";
import {FooterService, NavBackService, TitleService} from "@synerty/peek-util";
import {titleBarLinks} from "../plugin-title-bar-links";


export function titleServiceFactory() {
    const service = new TitleService();
    service.setLinks(titleBarLinks);
    return service;
}

export function footerServiceFactory() {
    const service = new FooterService();
    service.setLinks([]);
    return service;
}


export let peekRootServices = [
    // Peek-Util
    {
        provide: TitleService,
        useFactory: titleServiceFactory
    },
    {
        provide: FooterService,
        useFactory: footerServiceFactory
    },
    NavBackService,

    // Ng2BalloonMsg
    Ng2BalloonMsgService,

    // Vortex Services
    VortexStatusService,
    VortexService
];

