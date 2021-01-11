import { Component, OnInit } from '@angular/core';

import { RsItem } from '../rsItem'
import { RsDataService } from '../rs-data.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  rsData : RsItem[];

  filteredRsData : RsItem[];

  constructor(private rsDataService: RsDataService) { }

  ngOnInit(): void {
    this.getRsData();
  }

  getRsData() :void{
    this.rsDataService.getRsFromJson().subscribe(
      rsData => {
        console.log(rsData);
        this.rsData = rsData;
      }
    );

  }

  searchtext: string;

  results: string[];

  search(event) {
      /*this.mylookupservice.getResults(event.query).then(data => {
          this.results = data;
      });*/

      let filtered : any[] = [];
        let query = event.query;
        for(let i = 0; i < this.rsData.length; i++) {
            let rsItem = this.rsData[i];
            if (rsItem.nom.toLowerCase().indexOf(query.toLowerCase()) == 0) {
                filtered.push(rsItem);
            }
        }

        this.results = filtered;

  }


  home_cards = [
    {
      image_src : "assets/images/home/card1.png",
      image_alt : "Accompagnement pédagogique",
      title : "Accompagnement pédagogique",
      text : "Laissez vous guider par les analyses thématiques réalisées par nos experts",
      action_text : "Découvrir les analyses",
      action_link : "/pedagogie",
    },
    {
      image_src : "assets/images/home/card2.png",
      image_alt : "Exploration autonome",
      title : "Exploration autonome",
      text : "Entrez dans nos jeux de données et affichez les données qui vous intéressent",
      action_text : "Découvrir les jeux de données",
      action_link : "/exploration",
    },
    {
      image_src : "assets/images/home/card3.png",
      image_alt : "Intégration à votre travail",
      title : "Intégration à votre travail",
      text : "Des API sont à votre disposition pour une intégration à votre travail",
      action_text : "Découvrir les API",
      action_link : "/api",
    },
  ]

}
