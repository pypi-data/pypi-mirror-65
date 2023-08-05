import {Component, Input} from "@angular/core";
import {ComponentLifecycleEventEmitter, TupleSelector} from "@synerty/vortexjs";
import {TitleService} from "@synerty/peek-util";


@Component({
    selector: 'peek-core-device-cfg',
    templateUrl: 'core-device-cfg.component.web.html',
    moduleId: module.id
})
export class CoreDeviceCfgComponent extends ComponentLifecycleEventEmitter {

    constructor(private titleService: TitleService) {
        super();
        this.titleService.setTitle('Core Device Config');

    }

}
