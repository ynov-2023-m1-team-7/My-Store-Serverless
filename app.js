const nodemailer = require('nodemailer');
require('dotenv').config();

const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: process.env.SMTP_PORT,
    secure: false,
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS
    }
});

exports.sendEmail = async (data) => { // Recevoir les données en un seul objet (par exemple : { nom, prenom, email })
  try {
    const { nom, prenom, email } = data; // Extraire les données

    const mailOptions = {
      from: email,
      to: process.env.ADMIN_EMAIL,
      subject: 'Information user',
      html: `<p>Information user:</p>
             <p>Nom: ${nom}</p>
             <p>Prénom: ${prenom}</p>
             <p>Email: ${email}</p>`
    };

    const info = await transporter.sendMail(mailOptions);
    console.log('Email envoyé: ', info.messageId);
    return { message: 'Email envoyé avec succès !' };
  } catch (error) {
    console.error('Erreur lors de l\'envoi de l\'e-mail: ', error);
    throw new Error('Erreur lors de l\'envoi de l\'e-mail');
  }
};


// /**
//  *
//  * Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
//  * @param {Object} event - API Gateway Lambda Proxy Input Format
//  *
//  * Context doc: https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-context.html 
//  * @param {Object} context
//  *
//  * Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
//  * @returns {Object} object - API Gateway Lambda Proxy Output Format
//  * 
//  */

// import SibApiV3Sdk from 'sib-api-v3-sdk';

// export const lambdaHandler = async (event, context) => { 

//     console.log(process.env.API_KEY, "env");

//     try {
//          let defaultClient = SibApiV3Sdk.ApiClient.instance;

//         let apiKey = defaultClient.authentications['api-key'];

//         apiKey.apiKey = process.env.API_KEY;

//         let apiInstance = new SibApiV3Sdk.ContactsApi();

//         let createContact = new SibApiV3Sdk.CreateContact();

//         const { email } = JSON.parse(event.body);

//         createContact.email = email;
//         createContact.listIds = [process.env.LIST_ID]

//         const data = await apiInstance.createContact(createContact);
//         if (data) {
//             return {
//                 'statusCode': 200,
//                 'body': JSON.stringify({
//                     message: 'success',
//                 })
//             }
//         }
//     } catch (err) {
//         console.log(err);
//         return err;
//     }
// };