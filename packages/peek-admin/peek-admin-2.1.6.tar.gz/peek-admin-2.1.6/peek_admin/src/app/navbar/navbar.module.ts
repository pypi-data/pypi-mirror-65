import {NgModule} from "@angular/core";
import {CommonModule} from "@angular/common";
import {RouterModule} from "@angular/router";
import {NavbarComponent} from "./navbar.component";
import {AngularFontAwesomeModule} from "angular-font-awesome";

@NgModule({
    exports: [NavbarComponent],
    imports: [
        AngularFontAwesomeModule,
        CommonModule,
        RouterModule
    ],
    declarations: [NavbarComponent],
})
export class NavbarModule {
}
