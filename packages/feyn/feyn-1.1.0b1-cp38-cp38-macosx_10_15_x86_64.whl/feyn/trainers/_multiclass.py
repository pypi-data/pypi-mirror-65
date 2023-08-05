from sklearn.model_selection import train_test_split
from IPython.display import display, clear_output
import numpy as np

class TrainingSet:
    def __init__(self, X, y) -> None:
        self.X = X
        self.y = y


class MulticlassTrainer():
    
    def __init__(self, qlattice, dataframe, output='target', validation_size=0.3, output_labels=None):
        
        if output not in dataframe:
            raise KeyError(f'Output column: {output} is not present in the Dataframe. Please provide the output column.')
        
        if output_labels is not None:
            nlabels, nclasses = len(output_labels), dataframe[output].nunique()
            if nlabels != nclasses:
                raise(ValueError("Output labels need to be equal to amount of classes in target. Got {} labels, but {} classes".format(nlabels, nclasses)))
        
        self.output_labels = output_labels
        
        self._init_data(dataframe, output, validation_size)

        self._init_qlattice(qlattice)

        self.qdict = dict()
    
    def _init_qlattice(self, qlattice):
        self.qlattice = qlattice
        
        self.input_registers = []
        self.output_register = self.qlattice.get_register(self.output)
        
        # Add input features 
        for feature in self.dataframe.columns.difference([self.output]):
            self.input_registers.append(self.qlattice.get_register(feature))

    def _init_data(self, dataframe, output, validation_size) -> None:
        self.dataframe = dataframe.copy()
        self.output = output
        self.validation_size = validation_size

        self.dataframe[output] = self.dataframe[self.output].astype(int) # Ensure good stuff
        
        train, validation = train_test_split(self.dataframe, test_size=validation_size, stratify=self.dataframe[self.output])
        
        train_X = train[train.columns.difference([self.output])]
        train_y = train[self.output]
        self.training = TrainingSet(train_X, train_y)

        validation_X = validation[validation.columns.difference([self.output])]
        validation_y = validation[self.output]
        self.validation = TrainingSet(validation_X, validation_y)

    def _getlabel(self, klazz):
        label = klazz
        if self.output_labels is not None:
            label = self.output_labels[klazz]
        return label
    
    def tune(self, epochs_per_pass=10, no_passes=1, steps=3, optimize=None):
        print("[Abzu MulticlassTrainer] beginning training")
        for pazz in range(no_passes):
            for klazz in self.dataframe[self.output].unique():
                # Get a label if it exists for pretty printing.
                label = self._getlabel(klazz)
                print('Training class {}'.format(label))
                
                # If we don't already have a graph, add one. Else, just tune the existing one
                if klazz not in self.qdict:
                    self.qdict[klazz] = self.qlattice.get_qgraph(self.input_registers, self.output_register, steps=steps)

                self.qdict[klazz] = self.qlattice.get_qgraph(self.input_registers, self.output_register, steps=steps)

                # Tune it!
                self.qdict[klazz].tune(self.training.X, self.training.y == klazz, epochs=epochs_per_pass, showgraph=False, loss='categorical_cross_entropy')

                if optimize != None:
                    self._optimize(klazz, optimize['epochs'], optimize['graphs_count'])

                self.qlattice.update(self.qdict[klazz].graphs[0])
            
            print("Pass no {} of {}".format(pazz+1, no_passes))
            
    def show_graphs(self, ensemble_no=None):
        klazzes = self.dataframe[self.output].unique()
        for klazz in klazzes:
            print("Graph(s) for {}".format(self._getlabel(klazz)))
            if ensemble_no is not None:
                for i in range(ensemble_no):
                    display(self.qdict[klazz].graphs[i])
            else:
                display(self.qdict[klazz].graphs[0])
    
    def _optimize(self, klazz, epochs=100, graphs_count=10):
        label = self._getlabel(klazz)
        print('Optimizing class {}'.format(label))
        
        self.qdict[klazz].graphs = self.qdict[klazz].graphs[:graphs_count]
        self.qdict[klazz].tune(self.training.X, self.training.y == klazz, epochs=epochs, showgraph=False, loss='categorical_cross_entropy')

    def optimze(self, epochs=100, graphs_count=10):
        print("[Abzu MulticlassTrainer] Start Optimizing")
        
        for klazz in self.dataframe[self.output].unique():
            # Get a label if it exists for pretty printing.
            label = self._getlabel(klazz)
            print('Optimizing class {}'.format(label))
            
            # If we don't already have a graph, add one. Else, just tune the existing one
            if klazz not in self.qdict:
                raise KeyError("Class not present in existing graphs. Please tune first.")
            
            self._optimize(klazz, epochs, graphs_count)

    def predict(self, input_data, ensemble_no=None):        
        input = input_data.copy()
        # I mean, just in case people be weird
        if self.output in input_data.columns:
            print("Found target column in predictive dataset. Removing.")
            input = input[input.columns.difference([self.output])]
        
        # Consider also validating input feature lengths. We know abzu is a bit weird when receiving too many inputs or too few.
        pred_array = []
        klazzes = sorted(self.dataframe[self.output].unique())
        for klazz in klazzes:
            pred_array.append(self._get_pred_for_class(input, klazz, ensemble_no))
            
        pred_array = np.array(pred_array)
        predictions = self._get_target_predictions(pred_array)
        
        return predictions
    
    def _get_pred_for_class(self, input, klazz, ensemble_no):
        # Mean over the top N graphs if running ensemble mode
        if ensemble_no is not None:
            deez_preds = []
            for g_i in range(ensemble_no):
                deez_preds.append(self.qdict[klazz].graphs[g_i].predict(input))
            return np.mean(np.array(deez_preds), axis=0)
        
        return self.qdict[klazz].graphs[0].predict(input)
    
    def _get_target_predictions(self, preds):
        classes = []
        for ix, val in enumerate(preds.T):
            # Funny thing: This will end up promoting something to a class if it's just the most likely class among all of the graphs. This is fine.
            classes.append(np.argmax(val))
        return np.array(classes)
        

## TODO:x
# Do something better with the epochs and showing graphs
# Ehhh, can't really split val sets inside if training with a remote qlattice
# Should I train one class fully and update, or all classes once and then updates (current)