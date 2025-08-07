import os
import base64
from dash import Input, Output, State, callback, ctx, dcc, html, no_update, ALL
import dash_mantine_components as dmc
from datetime import datetime

UPLOAD_FOLDER = "data/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@callback(
    Output("notification-container", "sendNotifications", allow_duplicate=True),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True
)
def save_uploaded_file(content, filename):
    if content is None:
        return no_update

    try:
        content_type, content_string = content.split(",")
        decoded = base64.b64decode(content_string)

        # On nettoie le nom de fichier pour éviter les problèmes
        safe_filename = filename.replace(" ", "_").replace("/", "_")
        safe_filename = safe_filename.split(".csv")[0]
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(UPLOAD_FOLDER, f"{safe_filename}_{now}.csv")

        with open(filepath, "wb") as f:
            f.write(decoded)

        return [{
            "action": "show",
            "title": "Succès",
            "message": "Fichier enregistré.",
            "autoClose": 3000,
            "withCloseButton": True
        }]
    except Exception as e:
        return [{
            "action": "show",
            "title": "Erreur",
            "message": f"Erreur lors de l'enregistrement : {str(e)}.",
            "autoClose": 3000,
            "withCloseButton": True,
        }]


@callback(
    Output("uploaded-csv-container", "children"),
    Input("import-url", "pathname"),
    Input("upload-data", "contents"),
    Input({"type": "delete-csv", "index": ALL}, "n_clicks"),
    State({"type": "delete-csv", "index": ALL}, "id"),
)
def display_uploaded_csv_list(_, __, delete_clicks, delete_id):
    csv_files = sorted([f for f in os.listdir("data") if f.endswith(".csv")])
    triggered = ctx.triggered_id
    if isinstance(triggered, dict) and triggered.get("type") == "delete-csv":
        filename = triggered.get("index")
        path = os.path.join("data", filename)
        if os.path.exists(path):
            os.remove(path)

    files = [f for f in os.listdir("data") if f.endswith(".csv")]
    if not files:
        return dmc.Text("Aucun fichier CSV trouvé.")

    rows = [
        dmc.TableTr([
            dmc.TableTd(i + 1),
            dmc.TableTd(f),
            dmc.TableTd(dmc.Button("X", id={"type": "delete-csv", "index": f}, radius="xl", variant="light"))
        ]) for i, f in enumerate(files)
    ]

    head = dmc.TableThead(
        dmc.TableTr([
            dmc.TableTh("#"),
            dmc.TableTh("Nom de fichier"),
            dmc.TableTh("Supprimer")
        ])
    )

    body = dmc.TableTbody(rows)
    caption = dmc.TableCaption("Fichiers CSV disponibles dans le dossier /data")

    return dmc.Table([
        head,
        body,
        caption
    ],
        striped=True,
        highlightOnHover=True,
        withTableBorder=True,
        withColumnBorders=True,
        horizontalSpacing="md",
        verticalSpacing="xs"
    )
