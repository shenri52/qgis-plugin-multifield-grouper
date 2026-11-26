# MultiField Grouper

[![QGIS](https://img.shields.io/badge/QGIS-3.28%2B-green)](https://qgis.org/)
[![Version](https://img.shields.io/badge/version-0.1.2-blue)](https://github.com/shenri52/qgis-plugin-multifield-grouper/releases)

## Français

**MultiField Grouper 0.1.2** crée une table récapitulative sans géométrie à partir d'un champ identifiant et de plusieurs champs de catégorie indépendants. Il est accessible depuis le menu **Extensions** et depuis la boîte à outils **Traitements** de QGIS.

### Exemple

**Source**

| ID | zone | type |
|---|---|---|
| A01 | Nord | Urbain |
| A02 | Sud | Rural |
| A03 | Nord | Rural |
| A04 | *(vide)* | *(vide)* |
| A05 | Nord | *(vide)* |

**Résultat**

| categorie | nb_elements | elements |
|---|---:|---|
| Nord | 3 | A01, A03, A05 |
| Rural | 2 | A02, A03 |
| Sud | 1 | A02 |
| Urbain | 1 | A01 |
| NULL | 1 | A04 |

Chaque champ de catégorie est analysé indépendamment : A01 apparaît donc dans les catégories Nord et Urbain. Un identifiant n'est compté qu'une seule fois dans chaque catégorie. Les entités dont tous les champs de catégorie sont vides sont regroupées dans la catégorie spéciale `NULL`.

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

### Historique des versions

- **0.1.2** — Correction de la compatibilité des énumérations Qt6 dans la fenêtre graphique et l'algorithme de traitement. Suppression du gestionnaire d'exception trop large signalé par Bandit dans la détection des valeurs vides. Compatibilité QGIS 3.28 conservée.
- **0.1.1** — Ajout d'un exemple complet de source et de résultat dans les métadonnées et cette documentation. L'exemple illustre le traitement indépendant des champs de catégorie, le comptage des identifiants uniques et le regroupement des valeurs vides dans `NULL`.

## English

**MultiField Grouper 0.1.2** creates a non-spatial summary table from one identifier field and several independent category fields. It is available from the QGIS **Plugins** menu and the **Processing** toolbox.

### Example

**Input**

| ID | zone | type |
|---|---|---|
| A01 | North | Urban |
| A02 | South | Rural |
| A03 | North | Rural |
| A04 | *(empty)* | *(empty)* |
| A05 | North | *(empty)* |

**Output**

| category | count | identifiers |
|---|---:|---|
| North | 3 | A01, A03, A05 |
| Rural | 2 | A02, A03 |
| South | 1 | A02 |
| Urban | 1 | A01 |
| NULL | 1 | A04 |

Each category field is processed independently, so A01 appears in both North and Urban. An identifier is counted only once within each category. Features with all category fields empty are grouped in the special `NULL` category.

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

### Version history

- **0.1.2** — Fixed Qt6 enum compatibility in the graphical dialog and Processing algorithm. Removed the broad exception handler reported by Bandit from empty-value detection. QGIS 3.28 compatibility is preserved.
- **0.1.1** — Added a complete input/output example to the plugin metadata and this documentation. The example demonstrates independent category-field processing, unique identifier counts, and grouping empty values in `NULL`.

## License

GPL-2.0-or-later.
