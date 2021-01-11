import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { PedaComponent } from './peda/peda.component';
import { ArticlesComponent } from './articles/articles.component';
import { ExplorationComponent } from './exploration/exploration.component';
import { ApiComponent } from './api/api.component';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'pedagogie', component: PedaComponent },
  { path: 'articles', component: ArticlesComponent },
  { path: 'exploration', component: ExplorationComponent },
  { path: 'api', component: ApiComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
