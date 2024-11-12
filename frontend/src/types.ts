export interface Item {
  id: number;
  name: string;
  category: string;
  price: number;
}

export interface ItemCreate {
  name: string;
  category: string;
  price: number;
}

export interface ItemsQuery {
  items: Item[],
  totalPrice: number
}

export interface ItemsCreateResponse {
  id: number;
  status: ItemsStatus;
}

export enum ItemsStatus {
  CREATED = 'created',
  UPDATED = 'updated',
}

// all search params are optional
// this is sent to FastAPI, so we are using snake case here to be compliant with Python naming
export interface SearchParams {
  dt_from: string,
  dt_to: string,
  category: string
}