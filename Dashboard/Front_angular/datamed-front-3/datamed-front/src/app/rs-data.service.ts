import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { map} from 'rxjs/operators';

import { RsItem } from './rsItem'

//import { RSDATA } from '../'

@Injectable({
  providedIn: 'root'
})
export class RsDataService {

  rsData : RsItem[];

  constructor(private httpClient: HttpClient) { }

  //parses text to numer, exclufind chars and returning zero if nothing usable
  toNumber(x) {
    const parsed = parseInt(x, 10);
    if (isNaN(parsed)) { return 0; }
    return parsed;
  }

  //maps json object to rsItem
  private rsItemFromJsonElem(jsonElem): RsItem{
    return {
        numero: jsonElem["Numéro"],
        etat: jsonElem["État"],
        circuit_en_rupture: jsonElem["Circuit en rupture"],
        classification: jsonElem["Classification"],
        indications: jsonElem["Indications"],
        nom: jsonElem["Nom"],
        cip: jsonElem["CIP"],
        dci: jsonElem["DCI"],
        code_ATC: jsonElem["Code ATC"],
        classe_therapeutique: jsonElem["Classe Therapeutique"],
        nom_laboratoire: jsonElem["Nom Laboratoire"],
        volume_ventes_ville:  this.toNumber(jsonElem["Volume Ventes Ville (boites)"]),
        volume_ventes_hopital:  this.toNumber(jsonElem["Volume Ventes Hôpital (boites)"]),
        causes: jsonElem["CAUSES"],
      }
  }

  private rsItemArrayFromJson(rawJson){
     return rawJson.map( jsonItem => this.rsItemFromJsonElem(jsonItem)) ;
  }

  //gets RS data from online json
  getRsFromJson(): Observable<RsItem[]>{
    //get observable from json
    let jsonRawObservable = this.httpClient.get<RsItem[]>("assets/mock_data/RS_json_nouveau_format.json");

    //define function to
    let formatJson = map( (jsonArray:any[]) => this.rsItemArrayFromJson(jsonArray)  );
    let jsonFormattedData = formatJson(jsonRawObservable);

    return jsonFormattedData;
  }

}
