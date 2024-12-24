const bcrypt=require('bcrypt')
const UserModel=require('../Models/User');
const jwt=require('jsonwebtoken')






const signup=async(req,res)=>{
    try{

        const {name,email,password}=req.body;
        const user= await UserModel.findOne({email});
        if(user){
            return res.status(400).json({message:"User is already exist,you can login",success:false});
        }
        const UserModel=new UserModel({name,email,password});
        UserModel.password=await bcrypt.hash(password,10);
        await UserModel.save();
        res.status(201).json({
            message:"Signup successfully",
            success:true

        })

    }catch(err){
        res.status(500).json({
            message:"Internal server error",
            success:false
        })

    }
}





const login=async(req,res)=>{
    try{

        const {email,password}=req.body;
        const user= await UserModel.findOne({email});
        const errormsg="Auth failed email or pasword is wrong";

        if(!user){
            return res.status(400).json({message:errormsg,success:false});
        }
        const isPassequal=await bcrypt.compare(password,user.password);
        if(!isPassequal){
            return res.status(403).json({message:errormsg, success:false});
        }

        const jwttoken=jwt.sign(
            {email:user.email, _id:user._id},
            process.env.JWT_SECRET,
            {expiresin:'24h'
        })

        res.status(200).json

    }catch(err){
        res.status(500).json({
            message:"Internal server error",
            success:false
        })

    }
}

module.exports={
    login,
    signup
}


