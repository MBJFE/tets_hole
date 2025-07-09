from pypylon import pylon
import cv2

# Initialiser le transport layer factory
tl_factory = pylon.TlFactory.GetInstance()

# Récupérer tous les périphériques connectés
devices = tl_factory.EnumerateDevices()

# Vérifier qu'on a au moins une caméra
if len(devices) == 0:
    raise pylon.RuntimeException("Aucune caméra Basler détectée.")

# Créer une liste d'objets caméras
cameras = pylon.InstantCameraArray(len(devices))

# Attribuer les caméras détectées à l'objet InstantCameraArray
for i, cam in enumerate(cameras):
    cam.Attach(tl_factory.CreateDevice(devices[i]))

# Démarrer l'acquisition en continu
cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

try:
    while cameras.IsGrabbing():
        for i, cam in enumerate(cameras):
            grabResult = cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                # Accès à l'image
                image = grabResult.Array

                # Afficher l'image avec OpenCV
                window_name = f"Camera {i}"
                cv2.imshow(window_name, image)

            grabResult.Release()

        # Sortir avec la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Arrêter et libérer les caméras
    cameras.StopGrabbing()
    cv2.destroyAllWindows()
