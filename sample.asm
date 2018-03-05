



;
FUNCTION_01:
        MOVLW   D'64              ; number of bytes in erase block
        MOVWF   0x00
        MOVLW   BUFFER_ADDR_HIGH  ; point to buffer
        MOVWF   FSR0L
        BRA     READ_BLOCK
        bra     MODIFY_WORD
        MOVWF   TBLPTRL
        dw      0x0064            ; 'd'
        tblrd*-

        ; code

READ_BLOCK:

        TBLRD*+                 ; read into TABLAT, and inc
        MOVF    TABLAT, W       ; get data
        DECFSZ  COUNTER         ; done?
        BRA     READ_BLOCK      ; repeat


MODIFY_WORD:

        MOVLW   DATA_ADDR_HIGH    ; point to buffer
        MOVWF   0x00
        MOVLW   DATA_ADDR_LOW
        MOVWF   FSR0L
        MOVLW   NEW_DATA_LOW      ; update buffer word
        MOVWF   POSTINC0
        MOVLW   NEW_DATA_HIGH
        MOVWF   INDF0
