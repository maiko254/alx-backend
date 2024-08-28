const express = require('express');
import { createClient } from "redis";
import { promisify } from 'util';

const app = express();
const port = 1245;

const client = createClient();

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
    const itemID = Number(req.params.itemId);
    const item = getItemById(itemID);
    if (item) {
        const reservedStock = await getCurrentReservedStock(itemID);
        item.currentQuantity = item.initialAvailableQuantity - reservedStock;
        res.json(item);
    } else {
        res.json({ status: 'Product not found' });
    }
});

app.get('/reserve_product/:itemId', async (req, res) => {
    const itemID = Number(req.params.itemId);
    const item = getItemById(itemID);
    if (item) {
        const reservedStock = await getCurrentReservedStock(itemID);
        if (item.initialAvailableQuantity - reservedStock > 0) {
            reserveStockByID(itemID, reservedStock + 1);
            res.json({ status: 'Reservation confirmed', itemId: itemID });
        } else {
            res.json({ status: 'Not enough stock available', itemId: itemID });
        }
    } else {
        res.json({ status: 'Product not found' });
    }
});
app.listen(port, () => {
    console.log(`app listening at http://localhost:${port}`);
});

function reserveStockByID(itemID, stock) {
  const item = getItemById(itemID);
  if (item) {
    client.set(`item.${itemID}`, stock);
  }
}

const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
]

async function getCurrentReservedStock(itemID) {
  const getAsync = promisify(client.get).bind(client);
  const reservedStock = await getAsync(`item.${itemID}`);
  return reservedStock ? parseInt(reservedStock, 10) : 0;
}

function getItemById(itemID) {
  return listProducts.find((item) => item.itemId === itemID);
}

export default app;
