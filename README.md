# Semantics Analyzer

**Semantics analyzer** is a tool that has been developed with the idea of helping researchers in the analysis and study of texts under the criteria of the _Semantics_ dimension of the sociological theory Legitimation Code Theory ([LCT](https://legitimationcodetheory.com/)). With it, researchers will be able, on the one hand, to analyze texts following the metrics dictated by the [_Semantics_](https://legitimationcodetheory.com/theory/semantics/) dimension, and on the other hand, to represent the results graphically to show the called "semantics waves".
The two metrics considered in this tool are "semantic density", SD, and "semantic gravity", SG, and the researcher can decide whether to use both or only one of them for the analysis.
On the other hand, two hierarchical levels of analysis have been proposed in this tool. The first one, in clauses as defined in the theory related to the Semantics dimension of LCT. The second one, in sets of clauses, called _super clauses_, and whose value is the mode of all the values of the set.  This second level has been created with the idea of grouping clauses belonging to the same context. Thus, if, for example, the researcher wants to determine the predominant value in each paragraph of a text, he can easily obtain it with this functionality.

## Requeriments 

Python 3.11.0 has been used for the development of the tool described in this repository. There is no assurance that the tool will continue to work with earlier versions. 

Also, the following list shows the tools and libraries required to run and compile the application. The installation of these packages has been done using the [pip](https://pip.pypa.io/en/stable/) tool.

```
Package                   Version
------------------------- ---------
matplotlib                3.6.2
nltk                      3.8.1
numpy                     1.23.5
pyinstaller               5.12.0
PyQt5                     5.15.7
scipy                     1.9.3
xmlschema                 2.3.0
```

## Compilation

If you want to recompile the application from the code, just go to the "**compiled_app**" folder and execute the following command:

```
pyinstaller -w -y -n "app" --icon=logo.ico --add-data=<Python_Path>"\Python311\Lib\site-packages\xmlschema\schemas;xmlschema\schemas" ../app/start_window.py
```

This will generate the executable and all its associated files in the "**dist/app**" folder. If there are any problems, first, execute the following command an then delete the "**build**" folder and run the previous command again.

```
pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib
```

## Usage: Window Structure

### Start window

When the user opens the application, a window like the one shown in the figure below will be displayed. The user will be asked to choose a folder to be used as the working directory. This working directory will be used as the default path to browse and save the rest of the project files.

<p align="center">
<img align="center" src="https://github.com/pablo-sanmillanf/TFG_LCT/assets/101637076/4cbe5624-cc8e-4458-9617-6002bb692260">
<br/>
<i>Start window</i>
</p>

In the text box highlighted as "1", the path that is currently defined as the working directory is shown. The user can manually type in the path to be used or click on the button highlighted as "2" to browse for a directory using the file system of the operating system being used. 

Once you have chosen the desired working directory and you want to start the text analysis, just click on the "OK" button highlighted with a "3". On the other hand, if you have decided not to use the application, pressing the "Cancel" button in box "3" will close the application.
In the event that a directory that does not exist has been manually typed in box "1" and the user presses the "OK" button, the tool will let the user know.
 
Once a valid directory has been chosen, the main window will appear, as explained in the section "Main Window". In addition, the selected directory will be checked for a folder structure as shown below, and if not, it will be generated automatically.

```
---root_dir
   |
   +---analysis
   |
   +---conf
   |       conf.conf
   |   
   \---graph
```

Each of these three folders will have a specific function, as detailed below:
* The "**analysis**" folder will be the one displayed by default when you want to perform the saving of the analysis files. 
* The "**conf**" folder will be used to store the configuration file with the user preferences for the main window. This file must not be edited, otherwise the chosen style preferences will be lost. This folder is the only mandatory folder of the three for the correct functioning of the application.
* The "**graph**" folder will be the default folder to be displayed when you want to save a snapshot of the graph displayed in the graphing window. 

### Main window

Once the desired working directory has been chosen, the window shown in the figure below will appear with an example text indicating the basic steps to start using the application.

<p align="center">
<img align="center" src="https://github.com/pablo-sanmillanf/TFG_LCT/assets/101637076/d3f08731-7363-4eb5-8f0c-274a21440036">
<br/>
<i>Main window</i>
</p>

In the boxed area with a "1", each line of text is surrounded by a rectangle, hereafter rect, with a gray fill color. Also, below each line there is a text, from now on descriptor, with the value "**SD~;SG~**". Finally, two yellow rectangles, hereinafter separators, can also be seen at the beginning and end of the text. These separators can be yellow or black. In the first case, the separators are delimiting two super clauses, and in the second, two normal clauses. Each clause has a descriptor and a rect associated with it and, depending on the value of the descriptor, the color of the associated rect will change. 
In case a clause occupies several lines, there will be a descriptor and a rect for each line occupied by the clause with the same value and color, respectively. 

To split and merge clauses and super clauses, use the context menu shown in the figure below, which is accessed with the right mouse button.

<p align="center">
<img align="center" width="250" src="https://github.com/pablo-sanmillanf/TFG_LCT/assets/101637076/1a506838-9df0-485b-bc89-9d93986925a2">
<br/>
<i>Context menu</i>
</p>

The functions that can be performed with this menu are:

* "**Split**". Splits the clause in two and a separator is created at the nearest free "space" character.
* "**Join**". If there is a separator nearby, it removes the separator and merges the two contiguous clauses. The value of this new clause will be the same as the old clause to the left of the removed separator. 
* "**Promote to super separator**". If a normal separator exists nearby it allows to convert it to a super separator. Thus, the super clause is split into two.
* "**Demote from super separator**". If there is a super separator nearby, it allows to convert it to a normal separator. Thus, the two contiguous super clauses are merged into one.

In addition, the user can also move the separators to the desired "space" character by dragging and dropping. In case it is positioned at the beginning or at the end of a line, a copy of the separator will appear at the beginning of the next line if it has been placed at the end of a line, or at the end of the previous line if it has been placed at the beginning of a line. This copy is equally selectable and when one of the two separators is moved, the other will disappear. 
It should be mentioned that the separators at the beginning and end of the text cannot be moved, nor can they be converted into normal separators.

On the other hand, to change the value of a clause, you must select its associated descriptor. After this, the part of the descriptor that can be changed will be highlighted. At this point, only the characters "**-**" and "**+**" are supported, as long as valid values ("**++**", "**+**", "**--**" or "**-**") are obtained. As an indication that the field is being edited, the characters will be underlined. In case SD and SG are being analyzed at the same time, once one of the parameters has been edited, to change to the other one, just press the "Enter" key. When all parameters have been edited, pressing the "Enter" key again will cause the user to exit the descriptor editing. 
In addition, the "Del" key can be used to delete the values that have been entered. When all valid characters ("**++**", "**+**", "**--**" or "**-**") have been deleted, the default value "**~**" will automatically appear.

As an example, after inserting some separators and changing some descriptors, a complete analysis of the example text is shown below.

<p align="center">
<img align="center" src="https://github.com/pablo-sanmillanf/TFG_LCT/assets/101637076/f9a0a6b0-d0f7-4bb3-ab35-8b6d12058dd7">
<br/>
<i>Example of analysis</i>
</p>

In addition to the functionalities associated with the analysis, described above, the main window has a series of menus (marked "2" in the "Main window" figure) that provide extra capabilities. This menus are:

* "**File**":
    * "**New…**". Permite empezar un nuevo análisis a partir de un fichero de texto que se buscará utilizando el sistema de busqueda de archivos del sistema operativo que se esté utilizando. 
    * "**Open…**". Permite abrir un análisis existente guardado previamente en el sistema de archivos. Estos fichero deberán tener una extensión "**.lct**".
    * "**Save**". Permite guardar los cambios realizados en el análisis actual. Si se está editando un análisis preexistente abierto con el submenú "Open…", este fichero se sobrescribirá con la información nueva. Si el análisis no pertenece a ningún fichero de análisis previo, se abrirá una nueva ventana para seleccionar la carpeta y el nombre del nuevo fichero de análisis.
    * "**Save as…**". Se utiliza para guardar los cambios realizados en el análisis actual en un fichero de análisis nuevo.
* "**Edit**":
    * "**Text size**". It is used to set the size of the text to be analyzed and the rest of the associated elements (separators, descriptors and rects). Once the change is made, all clauses, separators, descriptors and recs will be repositioned to fit the new size.
    * "**Rects colors**". It is used to set the fill color of the rects for the different values that the associated descriptors can take. When this submenu is selected, a window with two tabs appears: "**SG or SD alone**" and "**SG and SD together**", as shown in the following figure. 
The tab on the left corresponds to the colors that the rects can take when analyzing SD or SG alone, while the tab on the right corresponds to the colors that the rects can take when analyzing SD and SG together. The "**Default color**" value corresponds to the color it will have as long as the associated descriptor does not have a valid value, i.e., as long as there is a "**~**" character. 
In order to change the color associated with a certain value, click on the box with the color in question. When you do this, a window will open in which you can select the desired color.
    <p align="center">
    <img align="center" width="600" src="https://github.com/pablo-sanmillanf/TFG_LCT/assets/101637076/72bac9e6-2c1d-4412-88dd-74cd2aa3fa53">
    <br/>
    <i>Rects colors dialog</i>
    </p>

    * "**Target**". It is used to set the parameter to be analyzed. The available options are "**SD**", "**SG**" or "**SD/SG**". The latter indicates that you want to analyze both parameters at the same time.
 * "**Tools**":
    * "**Split in sentences**". It is used to divide the text being analyzed into sentences automatically, setting a separator between each sentence. This action eliminates all previous analysis, so it should be used only at the beginning of the process or if you want to completely overwrite what was previously done.
 * "**Window**":
    * "**Run Plotter**". This submenu is used to open the graph window, detailed in the "**Graph Window**" section. This action can only be performed if the complete analysis of the text has been performed. If this submenu has already been selected previously and the graph window is already visible, the changes made in the analysis in the main window are not automatically updated, so you must select this submenu again to refresh the data displayed.
 * "**Help**". It is used to redirect the user to the GitHub used for this project, where the source code and a copy of the user manual are hosted.

Finally, when the user wants to leave the application, if changes have been made to the analysis that have not been saved, the user will be asked if these changes should be saved.
If the user still wants to leave the application and has made changes to the text size or rect colors, he will be asked if he wants to save these settings for the next time he uses the application.

### Graph Window

Once the text analysis has been completed in the main window, the graphing window can be accessed to view the results of the analysis, called "**semantics waves**".

<p align="center">
<img align="center" src="https://github.com/pablo-sanmillanf/TFG_LCT/assets/101637076/37195815-12aa-4dd4-86df-83f6c82f781e">
<br/>
<i>Graph window</i>
</p>

This window is composed of three components: the text that has been analyzed, which appears in the left column of the screen (marked with a "1"), the results of the analysis or "semantics waves", located on the right of the window (marked with a "2") and a slider bar (marked with a "3") with which to move along the graph. In addition, the user can also move around by dragging with the mouse within the graph itself.

Also, in case you want to determine to which part of the text corresponds to a certain instant of the graph, the user only has to click on any point of the vertical line that represents that instant. At that moment, the part of the text to which the selected instant refers will be highlighted at the top of the left column. 
<p align="center">
<img align="center" src="https://github.com/pablo-sanmillanf/TFG_LCT/assets/101637076/c6bcb709-8d07-4453-9cdd-47013a12ea84">
<br/>
<i>Example of instant selected in the graph window</i>
</p>

On the other hand, like the main window, the graph window has a series of menus (marked with a "4" in the figure "**Graph window**") that provide it with extra functionalities. These menus are:

*	"**File**":
    *	"**Save Visible Chart as Image**". It is used to save as an image the graph currently being viewed (the boxed area with the number "2" in the "**Graph window**"). When selected, a window will appear in which the user can choose the path and name of the desired image.
 * "**Edit**":
    * "**Visible points**". It is used to determine the number of instants to be displayed at a time on the graph between 1 and 50.
    * "**Target**". It is used to indicate which of the two levels of hierarchy of analysis you want to see in the graphs (clauses or super clauses).
 * "**View**":
    * "**Visibility**". It is used to indicate which parameters of the analysis are represented in the graph: SG, SD, both or none. If the analysis in the main window had been performed only for SD or SG, in this submenu only that option would appear as selectable, while the other would be disabled.
 * "**Help**". As in the main window, it is used to redirect the user to the GitHub used for this project, where the source code and a copy of the user manual are hosted.
