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


    fun detectPothole(): Pair<String, Int>? {
        return if (peaks["ACZ"]!!.indexOf(1) > peaks["ACZ"]!!.indexOf(-1) || peaks["DIS"]!!.indexOf(1) > peaks["DIS"]!!.indexOf(-1)){
            Pair("Pothole", peaks["ACZ"]!!.count{it != 0} + peaks["DIS"]!!.count{it != 0})
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

    fun detectSpeedBump() : Pair<String, Int>? {
        return if (peaks["ACZ"]!!.indexOf(1) < peaks["ACZ"]!!.indexOf(-1) || peaks["DIS"]!!.indexOf(1) < peaks["DIS"]!!.indexOf(-1)){
            Pair("Speedbump", peaks["ACZ"]!!.count{it != 0} + peaks["DIS"]!!.count{it != 0})
        } else {
            null
        }
    }

    fun detectCrash() : Pair<String, Int>? {
        for (key in listOf("ACX", "ACY", "ACZ")) {
            for (value in data[key]!!) {
                if (abs(value) > 100) {
                    return Pair("Crash", peaks["ACZ"]!!.count{it != 0} + peaks["DIS"]!!.count{it != 0})
                }
            }
        }
        return null
    }

    fun classifyIncident() : Pair<String, Int>? {
        smoothData()
        findPeaks()
        Log.d("Peaks", peaks.toString())
        val accident = detectCrash()

        if (accident != null) {
            Log.d("Classification", accident.toString())
            return accident
        }
        val pothole = detectPothole()
        if (pothole != null) {
            Log.d("Classification", pothole.toString())
            return pothole
        }
        val speedBump = detectSpeedBump()
        if (speedBump != null) {
            Log.d("Classification", speedBump.toString())
            return speedBump
        }
        Log.d("Classification", "None")

        return null
    }

}