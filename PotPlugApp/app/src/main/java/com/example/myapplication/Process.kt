package com.example.myapplication

import android.util.Log
import java.lang.Math.pow
import kotlin.math.abs
import kotlin.math.pow
import kotlin.math.sqrt

class Process (map : MutableMap<String, List<Float>>) {

    private var data = map
    private var peaks = mutableMapOf<String,List<Int>>()


    fun findPeaks() {
        for (key in data.keys) {
            val list = data[key]
            if (list != null) {
                val mean = list.average().toFloat()
                val detrended = list.map { (it - mean).toFloat() }
                Log.d("Detrended", key + " " + detrended.toString())
                Log.d("Mean", key + " " + mean.toString())
                val variance = sqrt(detrended.map { pow(it.toDouble(), 2.0) }.average().toFloat())
                Log.d("Variance", key + " " + variance.toString())
                peaks[key] = detrended.map {
                    when (abs(it) > 4 * variance) {
                        true -> if (it > 0) 1 else -1
                        false -> 0
                    }
                }
            }
        }
    }


    fun detectPothole(): Pair<String, String>? {
        return if (peaks["ACZ"]!!.indexOf(1) > peaks["ACZ"]!!.indexOf(-1) || peaks["DIS"]!!.indexOf(1) > peaks["DIS"]!!.indexOf(-1)){
            Pair("Pothole", "Pothole detected")
        } else {
            null
        }
    }

    fun smoothData() {
        for (key in data.keys) {
            val list = data[key]
            if (list != null) {
                val newList = mutableListOf<Float>()
                for (i in 0 until list.size - 4) {
                    newList.add((list[i] + list[i + 1] + list[i + 2] + list[i + 3]) / 4) // moving average with windows size of 4
                }
                data[key] = newList
            }
        }
    }

    fun calculateDerivative() {
        for (key in data.keys) {
            val list = data[key]
            if (list != null) {
                val newList = mutableListOf<Float>()
                for (i in 0 until list.size - 1) {
                    newList.add(list[i + 1] - list[i])
                }
                data[key] = newList
            }
        }
    }

    fun detectSpeedBump() : Pair<String, String>? {
        return if (peaks["ACZ"]!!.indexOf(1) < peaks["ACZ"]!!.indexOf(-1) || peaks["DIS"]!!.indexOf(1) < peaks["DIS"]!!.indexOf(-1)){
            Pair("Speedbump", "Speedbump detected")
        } else {
            null
        }
    }

    fun detectCrash() : Pair<String, String>? {
        for (key in listOf("ACX", "ACY", "ACZ")) {
            for (value in data[key]!!) {
                if (abs(value) > 100) {
                    return Pair("Crash", "Crash detected")
                }
            }
        }
        return null
    }

    fun classifyIncident() : Pair<String, String>? {
        smoothData()
        findPeaks()
        Log.d("Peaks", peaks.toString())
        val accident = detectCrash()

        if (accident != null) {
            Log.d("Classification", "Crash detected")
            return accident
        }
        val pothole = detectPothole()
        if (pothole != null) {
            Log.d("Classification", "Pothole detected")
            return pothole
        }
        val speedBump = detectSpeedBump()
        if (speedBump != null) {
            Log.d("Classification", "Speed bump detected")
            return speedBump
        }
        Log.d("Classification", "None")

        return null
    }

}