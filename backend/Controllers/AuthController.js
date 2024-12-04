const bcrypt=require('bcrypt')
const UserModel=require('../Models/User');






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

module.exports={
    signup
}