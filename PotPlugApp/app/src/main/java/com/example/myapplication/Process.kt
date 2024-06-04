package com.example.myapplication

import android.util.Log
import java.lang.Math.pow

class Process (map : MutableMap<String, List<Float>>) {

    private val data = map

    fun detectPothole() : Pair<String, String>? {
        val x = data["ACX"]?.average()
        val y = data["ACY"]?.average()
        val z = data["ACZ"]?.average()
        Log.d("Speed", "X: $x, Y: $y, Z: $z")
        if (x != null && y != null && z != null) {
            if (x < 7 && y < 2 && z < 3) {
                return Pair("Pothole", (pow(x, 2.0) + pow(y, 2.0) + pow(z, 2.0)).toString())
            }
        }
        return null
    }

    fun detectSpeedBump() : Pair<String, String>? {
        val x = data["ACX"]?.average()
        val y = data["ACY"]?.average()
        val z = data["ACZ"]?.average()
        if (x != null && y != null && z != null) {
            if (x < 0 && y < 0 && z < 7) {
                return Pair("Speedbump", (pow(x, 2.0) + pow(y, 2.0) + pow(z, 2.0)).toString())
            }
        }
        return null
    }

    fun detectCrash() : Pair<String, String>? {
        val x = data["ACX"]?.average()
        val y = data["ACY"]?.average()
        val z = data["ACZ"]?.average()
        Log.d("Crash", "X: $x, Y: $y, Z: $z")
        if (x != null && y != null && z != null) {
            if (x > 1.5 && y < 1.5 && z < 1.5) {
                return Pair("Crash", (pow(x, 2.0) + pow(y, 2.0) + pow(z, 2.0)).toString())
            }
        }
        return null
    }

    fun classifyIncident() : Pair<String, String>? {
        val pothole = detectPothole()
        if (pothole != null) {
            return pothole
        }
        val speedBump = detectSpeedBump()
        if (speedBump != null) {
            return speedBump
        }
        val accident = detectCrash()
        if (accident != null) {
            return accident
        }
        return null
    }

}