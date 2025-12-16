# Solución del Juego de Canicas (Triángulo)

Este es un juego de canicas con reglas similares a las damas: si saltas sobre una canica, la eliminas.  
El acomodo inicial es el siguiente:

```
          1
        2   3
      4   5   6
    7   8   9   10
 11  12  13  14  15
```

El hueco **15** estaba vacío al inicio.

---

## Pasos a seguir

1. **6 → 15**  _(salta sobre 10)_  
2. **1 → 6**   _(salta sobre 3)_  
3. **8 → 10**  _(salta sobre 9)_  
4. **2 → 9**   _(salta sobre 5)_  
5. **7 → 2**   _(salta sobre 4)_  
6. **10 → 3**  _(salta sobre 6)_  
7. **14 → 5**  _(salta sobre 9)_  
8. **3 → 8**   _(salta sobre 5)_  
9. **12 → 14** _(salta sobre 13)_  
10. **15 → 13** _(salta sobre 14)_  
11. **13 → 4** _(salta sobre 8)_  
12. **2 → 7**  _(salta sobre 4)_  
13. **11 → 4** _(salta sobre 7)_  

---