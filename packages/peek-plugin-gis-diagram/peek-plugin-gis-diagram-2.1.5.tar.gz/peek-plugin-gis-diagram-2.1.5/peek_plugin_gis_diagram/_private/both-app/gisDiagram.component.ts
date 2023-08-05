import {Component} from "@angular/core";
import {TitleService} from "@synerty/peek-util";

import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";

@Component({
    selector: 'plugin-gis-diagram',
    templateUrl: 'gisDiagram.component.web.html',
    moduleId: module.id
})
export class GisDiagramComponent extends ComponentLifecycleEventEmitter {

    constructor(private titleService:TitleService) {
        super();

        this.titleService.setTitle("GIS Diagram");

    }


}
