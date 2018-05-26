import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { Component, Input } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { ChartsModule } from 'ng2-charts';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { FlagDashboardComponent } from './flag-dashboard/flag-dashboard.component';
import { DatavisDashboardComponent } from './datavis-dashboard/datavis-dashboard.component';
import { ConfigDashboardComponent } from './config-dashboard/config-dashboard.component';
import { AboutComponent } from './about/about.component';
import { FlagsByDatastreamComponent } from './flags-by-datastream/flags-by-datastream.component';
import { NameComponent } from './name/name.component';
import { LineGraphComponent } from './datavis-dashboard/line-graph/line-graph.component';
import { DemoComponent } from './demo/demo.component';
import { DatasourceConfigComponent } from './config-dashboard/datasource-config/datasource-config.component';
import { TestConfigurationComponent } from './config-dashboard/test-configuration/test-configuration.component';
import { HistoryTrackerComponent } from './config-dashboard/test-configuration/history-tracker/history-tracker.component';



const appRoutes: Routes = [
  { path: 'flag', component: FlagDashboardComponent },
  { path: 'flag/:id', component: FlagsByDatastreamComponent },
  { path: 'datavis', component: DatavisDashboardComponent },
  { path: 'config', component: ConfigDashboardComponent },
  { path: 'about', component: AboutComponent },
  { path: 'demo', component: DemoComponent},
  { path: 'datasourceconfig', component: DatasourceConfigComponent},
  { path: 'testconfig', component: TestConfigurationComponent},
  { path: '**', redirectTo: '/flag', pathMatch: 'full' },
];


@NgModule({
  declarations: [
    AppComponent,
    NavBarComponent,
    FlagDashboardComponent,
    DatavisDashboardComponent,
    ConfigDashboardComponent,
    AboutComponent,
    FlagsByDatastreamComponent,
    NameComponent,
    LineGraphComponent,
    DemoComponent,
    DatasourceConfigComponent,
    TestConfigurationComponent,
    HistoryTrackerComponent
  ],
  imports: [
    HttpClientModule,
    ChartsModule,
    BrowserModule,
    RouterModule.forRoot(appRoutes),
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
