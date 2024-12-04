const express = require('express');
const app = express();
const bodyParser=require('body-parser')
const cors=require('cors');
const AuthRouter=require('./Routes/AuthRouter')

require('dotenv').config();
require('./Models/db'); // Ensure database connection is established

const PORT = process.env.PORT || 3000;

app.get('/ping', (req, res) => {
    res.send('pong');
});

app.use(bodyParser.json());
app.use(cors());
app.use('/auth',AuthRouter);

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
