import {CommonModule} from "@angular/common";
import {NgModule} from "@angular/core";
import {Routes} from "@angular/router";
// Import a small abstraction library to switch between nativescript and web
import {PeekModuleFactory} from "@synerty/peek-util-web";
// Import the default route component
import {GisDiagramComponent} from "./gisDiagram.component";
// Import the required classes from VortexJS
import {
    TupleActionPushNameService,
    TupleActionPushOfflineService,
    TupleActionPushService,
    TupleDataObservableNameService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService
} from "@synerty/vortexjs";
// Import the names we need for the
import {
    gisDiagramFilt,
    gisDiagramObservableName,
    gisDiagramTupleOfflineServiceName
} from "@peek/peek_plugin_gis_diagram/_private/PluginNames";
import {ShowDiagramComponent} from "./show-diagram/show-diagram.component";
// Import the names we need for the
import {gisDiagramActionProcessorName} from "@peek/peek_plugin_gis_diagram/_private";
import {PeekPluginDiagramModule} from "@peek/peek_plugin_diagram";

// Import the names we need for the


export function tupleActionPushNameServiceFactory() {
    return new TupleActionPushNameService(
        gisDiagramActionProcessorName, gisDiagramFilt);
}

export function tupleDataObservableNameServiceFactory() {
    return new TupleDataObservableNameService(
        gisDiagramObservableName, gisDiagramFilt);
}

export function tupleOfflineStorageNameServiceFactory() {
    return new TupleOfflineStorageNameService(gisDiagramTupleOfflineServiceName);
}

// Define the child routes for this plugin
export const pluginRoutes: Routes = [
    {
        path: '',
        pathMatch: 'full',
        component: GisDiagramComponent
    }

];

// Define the root module for this plugin.
// This module is loaded by the lazy loader, what ever this defines is what is started.
// When it first loads, it will look up the routs and then select the component to load.
@NgModule({
    imports: [
        CommonModule,
        PeekModuleFactory.RouterModule,
        PeekModuleFactory.RouterModule.forChild(pluginRoutes),
        ...PeekModuleFactory.FormsModules,
        PeekPluginDiagramModule
    ],
    exports: [],
    providers: [
        TupleActionPushOfflineService, TupleActionPushService, {
            provide: TupleActionPushNameService,
            useFactory: tupleActionPushNameServiceFactory
        },
        TupleOfflineStorageService, {
            provide: TupleOfflineStorageNameService,
            useFactory: tupleOfflineStorageNameServiceFactory
        },
        TupleDataObserverService, TupleDataOfflineObserverService, {
            provide: TupleDataObservableNameService,
            useFactory: tupleDataObservableNameServiceFactory
        },
    ],
    declarations: [GisDiagramComponent, ShowDiagramComponent]
})
export class GisDiagramModule {
}
