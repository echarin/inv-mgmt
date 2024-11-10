export enum Category {
  stationery = "stationery",
  gift = "gift"
}
export interface Item {
  id: number;
  name: string;
  category: Category;
  price: number;
}

export interface ItemCreate {
  name: string;
  category: Category;
  price: number;
}

export interface ItemsQuery {
  items: Item[],
  totalPrice: number
}