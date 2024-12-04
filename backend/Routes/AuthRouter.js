const { signup } = require('../Controllers/AuthController');
const {signupvalidation} =require('../Middlewares/AuthValidation')
const router=require('express').Router();

router.post('/login',(req,res)=>{
    res.send('login success');
})

router.post('/signup',signupvalidation, signup)

module.exports=router;