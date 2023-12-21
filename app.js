require('dotenv').config();

const API_KEY = process.env.BREVO_API_KEY;

exports.sendEmail = async (data) => {
  try {
    const fetch = (await import('node-fetch')).default; 

    const { nom, prenom, email } = data;

    const emailData = {
      sender: {
        name: `${nom} ${prenom}`,
        email: email
      },
      to: [
        {
          email: process.env.ADMIN_EMAIL,
          name: 'GROLLEMUND Kyllian'
        }
      ],
      subject: 'Informations utilisateur',
      htmlContent: `
        <p>Informations utilisateur :</p>
        <p>Nom : ${nom}</p>
        <p>Prénom : ${prenom}</p>
        <p>Email : ${email}</p>
      `
    };
  
    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'api-key': API_KEY
      },
      body: JSON.stringify(emailData)
    };

    const endpoint = 'https://api.brevo.com/v3/smtp/email';

    const response = await fetch(endpoint, requestOptions);
    const result = await response.json();

    console.log('Email envoyé: ', result);
    return { message: 'Email envoyé avec succès !' };
  } catch (error) {
    console.error('Erreur lors de l\'envoi de l\'e-mail: ', error);
    throw new Error('Erreur lors de l\'envoi de l\'e-mail');
  }
};
