// const mongoose=require('mongoose');
// const mongo_url=process.env.MONGO_CONN;

// mongoose.connect(mongo_url)
//     .then(()=>{
//         console.log('Connected to MongoDB');
//     }).catch((err)=>{
//         console.log("MongoDB Connection Error:", err);
//     })


const mongoose = require('mongoose');
const mongo_uri = process.env.MONGO_CONN;

if (!mongo_uri) {
    console.error("MongoDB connection string (MONGO_CONN) is missing in the .env file.");
    process.exit(1);
}

mongoose.connect(mongo_uri, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => {
        console.log('Connected to MongoDB');
    })
    .catch((err) => {
        console.error("MongoDB Connection Error:", err);
        process.exit(1);
    });
