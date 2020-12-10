import { TestBed } from '@angular/core/testing';

import { JsonToDataService } from './json-to-data.service';

describe('JsonToDataService', () => {
  let service: JsonToDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(JsonToDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
