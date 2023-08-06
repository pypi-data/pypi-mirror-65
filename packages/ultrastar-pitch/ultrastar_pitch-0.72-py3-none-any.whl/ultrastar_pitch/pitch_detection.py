#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file          pitch_detection.py
@brief         calculate the pitches of a timed USDX file
@author        paradigm
"""

import os
import sys
import numpy as np
from project_parser import ProjectParser
from preprocessing import AverageFourier
from classification import SlidingHarmonic, NeuronalNetwork

class PitchDetection:
    """ calculate the pitches of a timed USDX file
    @param method  analysing method for pitch detection
    """
    pitch_map = {0 : "C_", 1 : "C#", 2 : "D_", 3 : "D#", 4 : "E_", 5 : "F_",
                 6 : "F#", 7 : "G_", 8 : "G#", 9 : "A_", 10 : "A#", 11 : "B_"}

    def __init__(self, method="neuronal"):
        # counter for naming training data
        self.__file_counter = 0
        # init project parser
        self.__notes = ProjectParser()
        # init data preprocessor
        self.__trafo = AverageFourier()
        # init pitch classifier
        if method == "neuronal":
            # use neuronal network classifier by default
            default_model = "keras_tf_1025_240_120_12_fft_0.model"
            if getattr(sys,'frozen',False):
                model = os.path.join(sys._MEIPASS, default_model)
            else:
                model_path = os.path.join(os.path.dirname(__file__), "models")
                self.__model = os.path.join(model_path, default_model)
                
            self.__clf = NeuronalNetwork(model)
        else:
            # provide sliding harmonic classifier as fallback
            self.__clf = SlidingHarmonic()

    @classmethod
    def convert_pitch_notation(cls, freq, form="short"):
        """ return the pitch corresponding to a given frequency in different formats\n
        @param freq  frequency of a pitch
        @param form  format of the output
        @return  pitch / octave of a given frequency
        """
        assert freq > 16.35, "frequency value is too small to define pitch"
        # calculate number of half steps from C0
        h = round(12*np.log2(freq / (440 * 2**(-4.75))))
        if form == "octave":
            # return numeric octave (0, 1, 2, ...)
            return int(h // 12)
        elif form == "ascii":
            # return pitch notation (C, Cis, D, ...)
            return cls.pitch_map[int(h % 12)]
        elif form == "numeric":
            # return long numeric pitch
            return int(round(h))
        else:
            # return short numeric pitch (0-11)
            return int(round(h % 12))
          
    def predict_pitches(self, proj_file, dest_file):
        """ load a USDX project file and auto predict the pitches
        @param proj_file  location of the timed USDX project file
        @param dest_file  location for the new USDX file with predicted pitches
        """
        pitches = []
        # load and parse project
        self.__notes.load_note_file(proj_file)
        # divide audio into pitch segments
        audio_segments = self.__notes.process_audio()
        # analyse each segment
        for segment in audio_segments:
            # transform segment into features for prediction
            features = self.__trafo.transform_audio_segment(segment)
            # predict pitch based on the choosen classifier
            pitches.append(self.__clf(features))
        self.__notes.update_pitches(pitches)
        self.__notes.save_note_file(dest_file)

    # helper function to yield and display statistical data        
    def get_accuracy(self):
        # create a list with for true and predicted pitches
        y_true = [u_dict["org_pitch"] for u_dict in self.__usdx_data]
        y_pred = [u_dict["calc_pitch"] for u_dict in self.__usdx_data]
        # calculate correctly predicted pitches
        matches = 0
        for y_t, y_p in zip(y_true, y_pred):
            if y_t == y_p:
                matches += 1      
        # print statistical data
        print(str(len(y_true)) + " samples")
        if (len(y_true)):
            print(str(matches / len(y_true) * 100) + "% accuracy\n")
        else:
            print()          
        # return sample vectors
        return y_true, y_pred
    
    # build_training accuracy with pretranscripted song
    def draw_confusion_matrix(self):
        # create a list with for true and predicted pitches
        y_true, y_pred = self.get_statistics()
        labels=list(self.pitch_map.values())      
        # calculate confusion matrix
        c_mat = np.zeros((len(labels),len(labels)))
        for y_t, y_p in zip(y_true, y_pred):
            c_mat[y_t][y_p] += 1         
        # print detailed confusion matrix
        print("pred", end="\t")
        for label in labels:
            print(label, end="\t")
        print("\ntrue") 
        for i, label in enumerate(labels):
            print(label, end="\t")
            for val in c_mat[i]:
                print(int(val), end="\t")
            print("")
    
    def get_distribution(self):
        pass
    
    # yield training data for deep learning
    def generate_training_data(self, data_dir, mode="original"):
        # print informative statistics
        self.get_statistics()
        # create subfolder
        for pitch in self.pitch_map:
            pitch_dir = os.path.join(data_dir, str(pitch).zfill(2))
            os.makedirs(pitch_dir, exist_ok=True)
        # create a csv file for each analysed pitch   
        for u_dict in self.__usdx_data:
            # only write data, if calculated and original pitch match
            if u_dict["org_pitch"] != u_dict["calc_pitch"] and mode == "filtered":
                continue
            # create data from calculated pitch
            if mode == "calc":
                folder = str(u_dict["calc_pitch"])
            # create data form original pitch
            else:
                folder = str(u_dict["org_pitch"])
                
            data_path = os.path.join(data_dir, folder.zfill(2), str(self.__file_counter))
            # do not overwrite already existing data
            if not os.path.exists(data_path + ".npy"):
                np.save(data_path, u_dict["avg_fft"])     
            self.__file_counter += 1
 
    # remove previously created training data
    def clear_training_data(self, data_dir):
        for pitch in self.pitch_map:
            pitch_dir = os.path.join(data_dir, str(pitch).zfill(2))
            if os.path.exists(pitch_dir):
                filelist = [x for x in os.listdir(pitch_dir) if x.endswith(".npy")]
                for file in filelist:
                    os.remove(os.path.join(pitch_dir, file))
                print("cleared " + pitch_dir)
        print()