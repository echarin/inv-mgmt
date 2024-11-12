import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@mui/material";
import React from "react";
import { ItemsQuery } from "../types";
import ItemRow from "./ItemRow";

interface ItemTableProps {
  itemsQuery: ItemsQuery | null;
  isFetchingItems: boolean;
}

const ItemTable: React.FC<ItemTableProps> = ({
  itemsQuery,
  isFetchingItems
}) => {
  const totalPrice = itemsQuery?.totalPrice || 0;
  const items = itemsQuery?.items || [];

  return (
    <TableContainer>
      {isFetchingItems ? (
        <Typography variant="body1" align="center" padding={2}>
          Fetching items...
        </Typography>
      ) : (
        <>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell align="left"><strong>Name</strong></TableCell>
                <TableCell align="center"><strong>Category</strong></TableCell>
                <TableCell align="right"><strong>Price</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={3} align="center">
                    No items to display.
                  </TableCell>
                </TableRow>
              ) : (
                items.map((item) => (
                  <ItemRow key={item.id} item={item} />
                ))
              )}
            </TableBody>
          </Table>
          <Typography variant="h6" align="right" padding={2}>
            Total price: ${totalPrice.toFixed(2)}
          </Typography>
        </>
      )}
    </TableContainer>
  );
};

export default ItemTable;