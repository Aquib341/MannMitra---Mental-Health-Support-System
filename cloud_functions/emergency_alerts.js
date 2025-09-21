// cloud_functions/emergencyAlerts.js
const functions = require('firebase-functions');
const admin = require('firebase-admin');
const twilio = require('twilio');

admin.initializeApp();

const twilioClient = twilio(
  functions.config().twilio.sid,
  functions.config().twilio.auth_token
);

exports.sendEmergencyAlert = functions.firestore
  .document('emergency_alerts/{alertId}')
  .onCreate(async (snapshot, context) => {
    const alertData = snapshot.data();
    const userId = alertData.userId;
    const message = alertData.message || 'I need help';
    
    try {
      // Get user's emergency contacts
      const contactsSnapshot = await admin.firestore()
        .collection('users')
        .doc(userId)
        .collection('emergency_contacts')
        .get();
      
      // Get user profile
      const userDoc = await admin.firestore()
        .collection('users')
        .doc(userId)
        .get();
      const userData = userDoc.data();
      
      // Send alerts to each contact
      const promises = [];
      
      contactsSnapshot.forEach(contactDoc => {
        const contact = contactDoc.data();
        
        // Send SMS via Twilio if phone number exists
        if (contact.phone) {
          const smsPromise = twilioClient.messages.create({
            body: `EMERGENCY ALERT from ${userData.displayName || 'A MannMitra user'}: ${message}. Please check on them immediately.`,
            from: functions.config().twilio.phone_number,
            to: contact.phone
          });
          promises.push(smsPromise);
        }
        
        // Send email if email exists (implement with SendGrid or similar)
        if (contact.email) {
          // Email implementation would go here
          console.log(`Would send email to ${contact.email}`);
        }
      });
      
      // Send push notification to user's devices
      const devicesSnapshot = await admin.firestore()
        .collection('users')
        .doc(userId)
        .collection('devices')
        .get();
      
      devicesSnapshot.forEach(deviceDoc => {
        const device = deviceDoc.data();
        if (device.fcmToken) {
          const message = {
            notification: {
              title: 'Emergency Alert Activated',
              body: 'Your emergency contacts have been notified. Help is on the way.'
            },
            token: device.fcmToken
          };
          const pushPromise = admin.messaging().send(message);
          promises.push(pushPromise);
        }
      });
      
      await Promise.all(promises);
      
      return { success: true };
    } catch (error) {
      console.error('Error sending emergency alerts:', error);
      return { error: error.message };
    }
  });