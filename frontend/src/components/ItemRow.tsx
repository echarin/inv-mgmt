import { TableCell, TableRow } from "@mui/material";
import React from "react";
import { Item } from "../types";
import { capitalise } from "../utils";

interface ItemRowProps {
  item: Item;
}

const ItemRow: React.FC<ItemRowProps> = ({ item }) => {
  return (
    <TableRow>
      <TableCell align="left">{item.name}</TableCell>
      <TableCell align="center">{capitalise(item.category)}</TableCell>
      <TableCell align="right">{`$${item.price.toFixed(2)}`}</TableCell>
    </TableRow>
  );
};

export default ItemRow;
