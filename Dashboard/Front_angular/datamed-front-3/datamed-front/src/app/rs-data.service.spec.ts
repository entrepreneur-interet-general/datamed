import { TestBed } from '@angular/core/testing';

import { RsDataService } from './rs-data.service';

describe('RsDataService', () => {
  let service: RsDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RsDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
