# MultiField Grouper

[![QGIS](https://img.shields.io/badge/QGIS-3.28%2B-green)](https://qgis.org/)

## Français

**MultiField Grouper** crée une table récapitulative à partir d'un champ identifiant et de plusieurs champs de catégorie indépendants. Il est accessible depuis le menu **Extensions** et depuis la boîte à outils **Traitements** de QGIS.

### Fonctionnement

- Chaque champ de catégorie est analysé indépendamment.
- Une entité peut donc être présente dans plusieurs catégories.
- Les identifiants sont dédupliqués à l'intérieur de chaque catégorie.
- Les identifiants vides sont ignorés.
- Si tous les champs de catégorie sont vides, l'identifiant est placé dans une catégorie spéciale `NULL`.
- Si une catégorie contient déjà le texte `NULL`, les valeurs réellement vides sont distinguées sous le libellé `NULL (valeurs vides)`.
- Les catégories sont triées alphabétiquement et les identifiants sont triés dans chaque liste.
- Les espaces en début et en fin des identifiants et des catégories sont supprimés.

La table comporte trois colonnes : `categorie`, `nb_elements` et `elements`.

### Utilisation

**Fenêtre graphique :** choisissez la couche, le champ identifiant, cochez un ou plusieurs champs de catégorie, puis choisissez une sortie temporaire, GeoPackage ou CSV.

**Traitements :** recherchez « Group features by multiple category fields » dans la boîte à outils. L'algorithme peut être utilisé dans le modeleur graphique et dans les traitements par lots.

### Installation

1. Téléchargez `multifield_grouper.zip` depuis la page [Releases](https://github.com/shenri52/qgis-plugin-multifield-grouper/releases).
2. Dans QGIS, ouvrez **Extensions → Installer/Gérer les extensions → Installer depuis un ZIP**.
3. Sélectionnez l'archive téléchargée.

Le workflow GitHub Actions construit et joint automatiquement l'archive à chaque Release publiée. Il ne publie pas directement l'extension sur le dépôt officiel QGIS : cette étape reste à effectuer dans le portail des extensions QGIS.

## English

**MultiField Grouper** creates a summary table from one identifier field and several independent category fields. It is available from the QGIS **Plugins** menu and the **Processing** toolbox.

### How it works

- Each category field is evaluated independently.
- A feature can therefore belong to several categories.
- Identifiers are deduplicated within each category.
- Empty identifiers are ignored.
- If every category field is empty, the identifier is assigned to a special `NULL` category.
- If a real category already contains the text `NULL`, empty values are distinguished as `NULL (valeurs vides)`.
- Categories and identifiers are sorted alphabetically.
- Leading and trailing whitespace is stripped from identifiers and category values.

The output table contains three columns: `categorie`, `nb_elements`, and `elements`.

### Usage

**Graphical dialog:** choose the input layer, identifier field, one or more category fields, and a temporary, GeoPackage, or CSV output.

**Processing:** find “Group features by multiple category fields” in the Processing toolbox. The algorithm supports the graphical modeler and batch processing.

### Installation

1. Download `multifield_grouper.zip` from the [Releases page](https://github.com/shenri52/qgis-plugin-multifield-grouper/releases).
2. In QGIS, open **Plugins → Manage and Install Plugins → Install from ZIP**.
3. Select the downloaded archive.

The GitHub Actions workflow builds and attaches the archive to every published Release. It does not publish the plugin directly to the official QGIS plugin repository; that upload remains a separate step.

## License

GPL-2.0-or-later.
