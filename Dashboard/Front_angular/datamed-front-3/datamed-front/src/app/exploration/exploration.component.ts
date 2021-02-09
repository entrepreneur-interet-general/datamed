import { Component, OnInit } from '@angular/core';

import { RsItem } from '../rsItem'
import { RsDataService } from '../rs-data.service';

@Component({
  selector: 'app-exploration',
  templateUrl: './exploration.component.html',
  styleUrls: ['./exploration.component.scss']
})
export class ExplorationComponent implements OnInit {

  rsData : RsItem[];

  filteredRsData : RsItem[];

  cols: any[];

  constructor(private rsDataService: RsDataService) { }

  ngOnInit(): void {
      this.getRsData();
      this.cols = [
            { field: 'nom', header: 'Nom', displayed:true },
            { field: 'nom_laboratoire', header: 'Labo', displayed:true, },
            { field: 'dci', header: 'DCI', displayed:true, nonSortable:true},
            { field: 'code_ATC', header: 'Code ATC', },
      ]
  }

  getRsData() :void{
    this.rsDataService.getRsFromJson().subscribe(
      rsData => {
        console.log(rsData);
        this.rsData = rsData;
      }
    );
  }

  getDispo(rsItem){
    return {text: "Rupture", class: "state-rupture"}
  }


}
