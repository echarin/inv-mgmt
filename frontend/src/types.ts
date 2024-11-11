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