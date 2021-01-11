import { Component, OnInit } from '@angular/core';

import {MenuItem} from 'primeng/api';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss']
})
export class NavComponent implements OnInit {

  items: MenuItem[];

  constructor() { }

  ngOnInit(): void {
    this.items = [
      {
              label: 'Accueil',
              routerLink : ['/home'],
            },
            {
                label: 'Pédagogie',
                routerLink : ['/pedagogie'],
                /*items: [{
                        label: 'New',
                        icon: 'pi pi-fw pi-plus',
                        items: [
                            {label: 'Project'},
                            {label: 'Other'},
                        ]
                    },
                    {label: 'Open'},
                    {label: 'Quit'}
                ]*/
            },
            {
                label: 'Analyses thématiques',
                routerLink : ['/articles'],
                //icon: 'pi pi-fw pi-pencil',
                /*items: [
                    {label: 'Delete', icon: 'pi pi-fw pi-trash'},
                    {label: 'Refresh', icon: 'pi pi-fw pi-refresh'}
                ]*/
            },
            {
                label: 'Jeux de données',
                routerLink : ['/exploration'],
                //icon: 'pi pi-fw pi-pencil',
                /*items: [
                    {label: 'Delete', icon: 'pi pi-fw pi-trash'},
                    {label: 'Refresh', icon: 'pi pi-fw pi-refresh'}
                ]*/
            },
            {
                label: 'API',
                routerLink : ['/api'],
                //icon: 'pi pi-fw pi-pencil',
                /*items: [
                    {label: 'Delete', icon: 'pi pi-fw pi-trash'},
                    {label: 'Refresh', icon: 'pi pi-fw pi-refresh'}
                ]*/
            },
            {
                label: 'Archives',
                //icon: 'pi pi-fw pi-pencil',
                /*items: [
                    {label: 'Delete', icon: 'pi pi-fw pi-trash'},
                    {label: 'Refresh', icon: 'pi pi-fw pi-refresh'}
                ]*/
            }
        ];
  }

}
