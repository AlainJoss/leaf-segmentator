import cv2
import os
import numpy as np
import streamlit as st


##### READ IMAGES #####

def read_images(folder_path):
        images = []
        for img_name in os.listdir(folder_path):
            img = read_img(folder_path, img_name)
            images.append(img)
            
        return images


def read_img(folder_path, img_name):
    return cv2.imread(f'{folder_path}/{img_name}')


##### EXTRACT CHANNEL #####

def extract_channels(images):
    for idx, img in enumerate(images):
        img_hsv = extract_HSV_channel(img)
        images[idx] = extract_H_channel(img_hsv)

def extract_HSV_channel(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def extract_H_channel(img_hsv):
    return img_hsv[:, :, 0]


##### CLUSTERING MASK #####

def clustering_mask(img, num_clusters):
    labels_reshaped = kmeans_plusplus(img, num_clusters)
    return second_largest_cluster_mask(labels_reshaped, num_clusters)
"""
def kmeans_plusplus(img, num_clusters): 
    pixel_values = np.float32(img.flatten())
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, num_clusters, None, criteria, attempts=20, flags=cv2.KMEANS_PP_CENTERS)
    # _, labels, centers = cv2.kmeans(pixel_values, num_clusters, None, criteria, CLUSTERING_REPEATS, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    labels_reshaped = labels.reshape(img.shape)
    return labels_reshaped
"""
def second_largest_cluster_mask(labels_reshaped, num_clusters):
    masks = [cv2.inRange(labels_reshaped, cluster_id, cluster_id) for cluster_id in range(num_clusters)]
    sizes = [cv2.countNonZero(mask) for mask in masks]
    second_largest_cluster_mask = masks[sorted(zip(sizes, range(num_clusters)), reverse=True)[1][1]]

    return second_largest_cluster_mask


def kmeans_plusplus(image_channel, num_clusters): 
    pixel_values = np.float32(image_channel.flatten())
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    labels_reshaped = labels.reshape(image_channel.shape)

    return labels_reshaped

##### MASKERS #####

def largest_component_mask(mask):
    mask = np.uint8(mask)
    num_labels, labels = cv2.connectedComponents(mask, connectivity=8)
    _, counts = np.unique(labels, return_counts=True)

    if num_labels <= 1:
        return mask # return the original mask if no components were found
    
    largest_component = np.argmax(counts[1:]) + 1
    largest_mask = np.uint8(labels == largest_component) * 255
    return largest_mask

def apply_mask(img, mask):
    return cv2.bitwise_and(img, img, mask=mask)


##### BLURRING #####

def cut_stem(masked_img, stop_distance, kernel_size):
    binary_img = gray_to_binary(masked_img)  # changed this line
    start_row = None
    end_row = None

    for row in range(binary_img.shape[0]):
        current_row = binary_img[row, :]
        non_zero_indices = np.nonzero(current_row)[0]
    
        if non_zero_indices.size > 0:
            if start_row is None:
                start_row = row
            
            pixel_distance = np.max(non_zero_indices) - np.min(non_zero_indices)
            
            if pixel_distance > stop_distance:
                end_row = row
                break

    if (start_row is not None and end_row is not None and start_row < end_row) or start_row != 0:
        stem_region = masked_img[start_row:end_row, :]  # changed this line
        blurred_stem = median_blur(stem_region, kernel_size)
        return np.vstack((masked_img[:start_row, :], blurred_stem, masked_img[end_row:, :]))  # changed this line
    else:
        return masked_img
    
def median_blur(stem_region, kernel_size):
    return cv2.medianBlur(stem_region, kernel_size)


##### COLOR CONVERTERS #####

def gray_to_binary(img):
    gray_img = bgr_to_gray(img)
    _, binary_img = cv2.threshold(gray_img, 1, 255, cv2.THRESH_BINARY)
    return binary_img

def bgr_to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)