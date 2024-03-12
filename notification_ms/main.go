package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"time"

	"cloud.google.com/go/firestore"
	"github.com/google/uuid"

	firebase "firebase.google.com/go"
	"firebase.google.com/go/messaging"
	_ "github.com/go-sql-driver/mysql"
	"github.com/joho/godotenv"
	"google.golang.org/api/option"
)

func main() {
	http.HandleFunc("/send-like-notification", sendLikeNotification)
	http.HandleFunc("/send-comment-notification", sendCommentNotification)
	http.HandleFunc("/send-friend-request-notification", sendFriendRequestNotification)
	http.HandleFunc("/send-friend-request-accept-notification", sendFriendRequestAcceptNotification)
	http.HandleFunc("/send-dm-notification", sendDMNotification)
	http.HandleFunc("/send-group-request-accept-notification", sendGroupRequestAcceptNotification)
	http.HandleFunc("/user/preferences", handleUserPreferences)
	http.HandleFunc("/user/devices", handleUserDevices)
	http.ListenAndServe(":8080", nil)
}

type Notification struct {
	ID               string    `json:"id"`
	SenderID         int       `json:"senderID"`
	ReceiverID       int       `json:"receiverID"`
	Token            string    `json:"token"`
	Title            string    `json:"title"`
	Body             string    `json:"body"`
	NotificationType string    `json:"notificationType"`
	SendTime         time.Time `json:"sendTime"`
	DeepLink         string    `json:"deepLink"`
}

func sendNotificationHandler(w http.ResponseWriter, r *http.Request) {
	var data struct {
		SenderID   int    `json:"senderID"`
		ReceiverID int    `json:"receiverID"`
		Token      string `json:"token"`
		Title      string `json:"title"`
		Body       string `json:"body"`
		Type       string `json:"notificationType"`
		DeepLink   string `json:"deepLink"`
	}
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		http.Error(w, "Error al decodificar el cuerpo de la solicitud", http.StatusBadRequest)
		return
	}

	// Llamar a la función para enviar la notificación
	if err := sendNotification(data.SenderID, data.ReceiverID, data.Token, data.Title, data.Body, data.Type, data.DeepLink); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Responder con un código de estado 200 OK
	w.WriteHeader(http.StatusOK)
}

func sendNotification(senderID, receiverID int, token, title, body, notificationType, deepLink string) error {
	err := godotenv.Load("C:/Users/fhcha/OneDrive/Documentos/UNConnect/Notificaciones/environment.env")
	if err != nil {
		// Manejar el error si no se puede cargar el archivo
		panic("Error loading environment file")
	}

	firebaseCredentials := os.Getenv("FIREBASE_CREDENTIALS")

	ctx := context.Background()
	opt := option.WithCredentialsFile(firebaseCredentials)
	app, err := firebase.NewApp(ctx, nil, opt)
	if err != nil {
		return fmt.Errorf("error initializing Firebase app: %v", err)
	}

	client, err := app.Messaging(ctx)
	if err != nil {
		return fmt.Errorf("error getting Messaging client: %v", err)
	}

	message := &messaging.Message{
		Notification: &messaging.Notification{
			Title: title,
			Body:  body,
		},
		Token: token,
	}

	_, err = client.Send(ctx, message)
	if err != nil {
		return fmt.Errorf("error sending message: %v", err)
	}

	if err := addNotificationToDB(app, senderID, receiverID, token, title, body, notificationType, time.Now(), deepLink); err != nil {
		return fmt.Errorf("error adding notification to database: %v", err)
	}

	return nil
}

func addNotificationToDB(app *firebase.App, senderID, receiverID int, token, title, body, notificationType string, sendTime time.Time, deepLink string) error {
	// Obtener una referencia a la base de datos de Firebase
	ctx := context.Background()
	client, err := app.Database(ctx)
	if err != nil {
		return fmt.Errorf("error obteniendo el cliente de la base de datos Firebase: %v", err)
	}

	// Generar un ID único para la notificación
	id := uuid.New().String()

	// Crear una instancia de Notification
	notification := Notification{
		ID:               id,
		SenderID:         senderID,
		ReceiverID:       receiverID,
		Token:            token,
		Title:            title,
		Body:             body,
		NotificationType: notificationType,
		SendTime:         sendTime,
		DeepLink:         deepLink,
	}

	// Convertir la notificación a JSON
	notificationJSON, err := json.Marshal(notification)
	if err != nil {
		return fmt.Errorf("error convirtiendo la notificación a JSON: %v", err)
	}

	// Escribir los datos en la base de datos de Firebase
	ref := client.NewRef("notifications").Child(id)
	if err := ref.Set(ctx, notificationJSON); err != nil {
		return fmt.Errorf("error escribiendo la notificación en la base de datos Firebase: %v", err)
	}

	return nil
}

func sendLikeNotification(w http.ResponseWriter, r *http.Request) {
	var data struct {
		ReceiverID int    `json:"receiverID"`
		Token      string `json:"token"`
	}
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		http.Error(w, "Error al decodificar el cuerpo de la solicitud", http.StatusBadRequest)
		return
	}

	if err := sendNotification(0, data.ReceiverID, data.Token, "Novedad de post", "¡Alguien acaba de dar like a tu post!", "Like", ""); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
}

func sendCommentNotification(w http.ResponseWriter, r *http.Request) {
	var data struct {
		ReceiverID int    `json:"receiverIDID"`
		Token      string `json:"token"`
	}
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		http.Error(w, "Error al decodificar el cuerpo de la solicitud", http.StatusBadRequest)
		return
	}

	if err := sendNotification(0, data.ReceiverID, data.Token, "Novedad de post", "¡Alguien acaba de comentar en tu post!", "Comment", ""); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
}

func sendFriendRequestNotification(w http.ResponseWriter, r *http.Request) {
	var data struct {
		ReceiverID int    `json:"receiverIDID"`
		Token      string `json:"token"`
	}
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		http.Error(w, "Error al decodificar el cuerpo de la solicitud", http.StatusBadRequest)
		return
	}

	if err := sendNotification(0, data.ReceiverID, data.Token, "Solicitud de amistad", "¡Acabas de recibir una nueva solicitud de amistad!", "Like", ""); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
}

func sendFriendRequestAcceptNotification(w http.ResponseWriter, r *http.Request) {
	var data struct {
		ReceiverID int    `json:"receiverIDID"`
		Token      string `json:"token"`
	}
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		http.Error(w, "Error al decodificar el cuerpo de la solicitud", http.StatusBadRequest)
		return
	}

	if err := sendNotification(0, data.ReceiverID, data.Token, "Solicitud de amistad", "¡Acaban de aceptar tu solicitud de amistad!", "DM", ""); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
}

func sendDMNotification(w http.ResponseWriter, r *http.Request) {
	var data struct {
		ReceiverID int    `json:"receiverIDID"`
		Token      string `json:"token"`
	}
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		http.Error(w, "Error al decodificar el cuerpo de la solicitud", http.StatusBadRequest)
		return
	}

	if err := sendNotification(0, data.ReceiverID, data.Token, "Mensaje directo", "¡Has recibido un mensaje directo!", "DM", ""); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
}

func sendGroupRequestAcceptNotification(w http.ResponseWriter, r *http.Request) {
	var data struct {
		ReceiverID int    `json:"receiverIDID"`
		Token      string `json:"token"`
	}
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		http.Error(w, "Error al decodificar el cuerpo de la solicitud", http.StatusBadRequest)
		return
	}

	if err := sendNotification(0, data.ReceiverID, data.Token, "Solicitud de entrada a un grupo", "¡Acaban de aceptar tu solicitud para ingresar en un grupo!", "DM", ""); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
}

func handleUserPreferences(w http.ResponseWriter, r *http.Request) {
	err := godotenv.Load("C:/Users/fhcha/OneDrive/Documentos/UNConnect/Notificaciones/environment.env")
	if err != nil {
		http.Error(w, "Error al cargar el archivo de entorno", http.StatusInternalServerError)
		return
	}

	firebaseCredentials := os.Getenv("FIREBASE_CREDENTIALS")

	ctx := context.Background()
	opt := option.WithCredentialsFile(firebaseCredentials)
	app, err := firebase.NewApp(ctx, nil, opt)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error inicializando la aplicación Firebase: %v", err), http.StatusInternalServerError)
		return
	}

	firestoreClient, err := app.Firestore(ctx)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error inicializando el cliente de Firestore: %v", err), http.StatusInternalServerError)
		return
	}

	switch r.Method {
	case http.MethodPost:
		var data struct {
			ReceiverID         int    `json:"receiverID"`
			NuevasPreferencias string `json:"nuevasPreferencias"`
		}
		if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
			http.Error(w, "Error al decodificar el cuerpo de la solicitud", http.StatusBadRequest)
			return
		}
		if err := addUserPreferences(firestoreClient, ctx, data.ReceiverID, data.NuevasPreferencias); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusOK)

	case http.MethodPut:
		var data struct {
			ReceiverID         int    `json:"receiverID"`
			NuevasPreferencias string `json:"nuevasPreferencias"`
		}
		if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
			http.Error(w, "Error al decodificar el cuerpo de la solicitud", http.StatusBadRequest)
			return
		}
		if err := updatePreferences(firestoreClient, ctx, data.ReceiverID, data.NuevasPreferencias); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusOK)

	case http.MethodGet:
		receiverIDStr := r.URL.Query().Get("receiverID")
		if receiverIDStr == "" {
			http.Error(w, "El parámetro receiverID es requerido", http.StatusBadRequest)
			return
		}
		receiverID, err := strconv.Atoi(receiverIDStr)
		if err != nil {
			http.Error(w, "El parámetro receiverID debe ser un número entero", http.StatusBadRequest)
			return
		}
		preferences, err := getPreferences(firestoreClient, ctx, receiverID)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		json.NewEncoder(w).Encode(map[string]string{"preferences": preferences})

	case http.MethodDelete:
		receiverIDStr := r.URL.Query().Get("receiverID")
		if receiverIDStr == "" {
			http.Error(w, "El parámetro receiverID es requerido", http.StatusBadRequest)
			return
		}
		receiverID, err := strconv.Atoi(receiverIDStr)
		if err != nil {
			http.Error(w, "El parámetro receiverID debe ser un número entero", http.StatusBadRequest)
			return
		}
		if err := deletePreferences(firestoreClient, ctx, receiverID); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusOK)

	default:
		http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
	}
}

func addUserPreferences(client *firestore.Client, ctx context.Context, receiverID int, nuevasPreferencias string) error {
	_, err := client.Collection("preferences").Doc(fmt.Sprintf("%d", receiverID)).Set(ctx, map[string]interface{}{
		"preferences": nuevasPreferencias,
	})
	if err != nil {
		return fmt.Errorf("error guardando las nuevas preferencias del usuario: %v", err)
	}
	return nil
}

func updatePreferences(client *firestore.Client, ctx context.Context, receiverID int, nuevasPreferencias string) error {
	_, err := client.Collection("preferences").Doc(fmt.Sprintf("%d", receiverID)).Set(ctx, map[string]interface{}{
		"preferences": nuevasPreferencias,
	})
	if err != nil {
		return fmt.Errorf("error actualizando las preferencias del usuario: %v", err)
	}
	return nil
}

func getPreferences(client *firestore.Client, ctx context.Context, receiverID int) (string, error) {
	doc, err := client.Collection("preferences").Doc(fmt.Sprintf("%d", receiverID)).Get(ctx)
	if err != nil {
		return "", fmt.Errorf("error obteniendo las preferencias del usuario: %v", err)
	}
	var data map[string]interface{}
	if err := doc.DataTo(&data); err != nil {
		return "", fmt.Errorf("error obteniendo los datos de las preferencias del usuario: %v", err)
	}
	preferences, ok := data["preferences"].(string)
	if !ok {
		return "", fmt.Errorf("error convirtiendo las preferencias del usuario a string")
	}
	return preferences, nil
}

func deletePreferences(client *firestore.Client, ctx context.Context, receiverID int) error {
	_, err := client.Collection("preferences").Doc(fmt.Sprintf("%d", receiverID)).Delete(ctx)
	if err != nil {
		return fmt.Errorf("error eliminando las preferencias del usuario: %v", err)
	}
	return nil
}

func handleUserDevices(w http.ResponseWriter, r *http.Request) {
	err := godotenv.Load("C:/Users/fhcha/OneDrive/Documentos/UNConnect/Notificaciones/environment.env")
	if err != nil {
		http.Error(w, "Error al cargar el archivo de entorno", http.StatusInternalServerError)
		return
	}

	firebaseCredentials := os.Getenv("FIREBASE_CREDENTIALS")

	ctx := context.Background()
	opt := option.WithCredentialsFile(firebaseCredentials)
	config := &firebase.Config{
		ProjectID: "unconnect-c4b57",
	}
	app, err := firebase.NewApp(ctx, config, opt)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error inicializando la aplicación Firebase: %v", err), http.StatusInternalServerError)
		return
	}

	firestoreClient, err := app.Firestore(ctx)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error inicializando el cliente de Firestore: %v", err), http.StatusInternalServerError)
		return
	}

	switch r.Method {
	case http.MethodPost:
		var data struct {
			ReceiverID int    `json:"receiverID"`
			Token      string `json:"token"`
		}
		if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
			http.Error(w, "Error al decodificar el cuerpo de la solicitud", http.StatusBadRequest)
			return
		}
		if err := registerDevice(firestoreClient, ctx, data.ReceiverID, data.Token); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusOK)

	case http.MethodGet:
		receiverIDStr := r.URL.Query().Get("receiverID")
		if receiverIDStr == "" {
			http.Error(w, "El parámetro receiverID es requerido", http.StatusBadRequest)
			return
		}
		receiverID, err := strconv.Atoi(receiverIDStr)
		if err != nil {
			http.Error(w, "El parámetro receiverID debe ser un número entero", http.StatusBadRequest)
			return
		}
		token, err := readDeviceToken(firestoreClient, ctx, receiverID)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		json.NewEncoder(w).Encode(map[string]string{"token": token})

	case http.MethodDelete:
		receiverIDStr := r.URL.Query().Get("receiverID")
		if receiverIDStr == "" {
			http.Error(w, "El parámetro receiverID es requerido", http.StatusBadRequest)
			return
		}
		receiverID, err := strconv.Atoi(receiverIDStr)
		if err != nil {
			http.Error(w, "El parámetro receiverID debe ser un número entero", http.StatusBadRequest)
			return
		}
		if err := deleteDevice(firestoreClient, ctx, receiverID); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusOK)

	default:
		http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
	}
}

func registerDevice(client *firestore.Client, ctx context.Context, receiverID int, token string) error {
	docRef := client.Collection("devices").Doc(strconv.Itoa(receiverID))

	_, err := docRef.Set(ctx, map[string]interface{}{
		"token": token,
	})
	if err != nil {
		return fmt.Errorf("error guardando el token del dispositivo: %v", err)
	}

	return nil
}

func readDeviceToken(client *firestore.Client, ctx context.Context, receiverID int) (string, error) {
	docRef := client.Collection("devices").Doc(strconv.Itoa(receiverID))

	doc, err := docRef.Get(ctx)
	if err != nil {
		return "", fmt.Errorf("error obteniendo el token del dispositivo: %v", err)
	}

	token, ok := doc.Data()["token"].(string)
	if !ok {
		return "", fmt.Errorf("el token del dispositivo no es un string")
	}

	return token, nil
}

func deleteDevice(client *firestore.Client, ctx context.Context, receiverID int) error {
	docRef := client.Collection("devices").Doc(strconv.Itoa(receiverID))

	_, err := docRef.Delete(ctx)
	if err != nil {
		return fmt.Errorf("error eliminando el token del dispositivo: %v", err)
	}

	return nil
}
