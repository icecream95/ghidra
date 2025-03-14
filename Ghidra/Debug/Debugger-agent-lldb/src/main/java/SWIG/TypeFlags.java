/* ###
 * IP: Apache License 2.0 with LLVM Exceptions
 */
package SWIG;


/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 4.0.2
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */


public final class TypeFlags {
  public final static TypeFlags eTypeHasChildren = new TypeFlags("eTypeHasChildren", lldbJNI.eTypeHasChildren_get());
  public final static TypeFlags eTypeHasValue = new TypeFlags("eTypeHasValue", lldbJNI.eTypeHasValue_get());
  public final static TypeFlags eTypeIsArray = new TypeFlags("eTypeIsArray", lldbJNI.eTypeIsArray_get());
  public final static TypeFlags eTypeIsBlock = new TypeFlags("eTypeIsBlock", lldbJNI.eTypeIsBlock_get());
  public final static TypeFlags eTypeIsBuiltIn = new TypeFlags("eTypeIsBuiltIn", lldbJNI.eTypeIsBuiltIn_get());
  public final static TypeFlags eTypeIsClass = new TypeFlags("eTypeIsClass", lldbJNI.eTypeIsClass_get());
  public final static TypeFlags eTypeIsCPlusPlus = new TypeFlags("eTypeIsCPlusPlus", lldbJNI.eTypeIsCPlusPlus_get());
  public final static TypeFlags eTypeIsEnumeration = new TypeFlags("eTypeIsEnumeration", lldbJNI.eTypeIsEnumeration_get());
  public final static TypeFlags eTypeIsFuncPrototype = new TypeFlags("eTypeIsFuncPrototype", lldbJNI.eTypeIsFuncPrototype_get());
  public final static TypeFlags eTypeIsMember = new TypeFlags("eTypeIsMember", lldbJNI.eTypeIsMember_get());
  public final static TypeFlags eTypeIsObjC = new TypeFlags("eTypeIsObjC", lldbJNI.eTypeIsObjC_get());
  public final static TypeFlags eTypeIsPointer = new TypeFlags("eTypeIsPointer", lldbJNI.eTypeIsPointer_get());
  public final static TypeFlags eTypeIsReference = new TypeFlags("eTypeIsReference", lldbJNI.eTypeIsReference_get());
  public final static TypeFlags eTypeIsStructUnion = new TypeFlags("eTypeIsStructUnion", lldbJNI.eTypeIsStructUnion_get());
  public final static TypeFlags eTypeIsTemplate = new TypeFlags("eTypeIsTemplate", lldbJNI.eTypeIsTemplate_get());
  public final static TypeFlags eTypeIsTypedef = new TypeFlags("eTypeIsTypedef", lldbJNI.eTypeIsTypedef_get());
  public final static TypeFlags eTypeIsVector = new TypeFlags("eTypeIsVector", lldbJNI.eTypeIsVector_get());
  public final static TypeFlags eTypeIsScalar = new TypeFlags("eTypeIsScalar", lldbJNI.eTypeIsScalar_get());
  public final static TypeFlags eTypeIsInteger = new TypeFlags("eTypeIsInteger", lldbJNI.eTypeIsInteger_get());
  public final static TypeFlags eTypeIsFloat = new TypeFlags("eTypeIsFloat", lldbJNI.eTypeIsFloat_get());
  public final static TypeFlags eTypeIsComplex = new TypeFlags("eTypeIsComplex", lldbJNI.eTypeIsComplex_get());
  public final static TypeFlags eTypeIsSigned = new TypeFlags("eTypeIsSigned", lldbJNI.eTypeIsSigned_get());
  public final static TypeFlags eTypeInstanceIsPointer = new TypeFlags("eTypeInstanceIsPointer", lldbJNI.eTypeInstanceIsPointer_get());

  public final int swigValue() {
    return swigValue;
  }

  public String toString() {
    return swigName;
  }

  public static TypeFlags swigToEnum(int swigValue) {
    if (swigValue < swigValues.length && swigValue >= 0 && swigValues[swigValue].swigValue == swigValue)
      return swigValues[swigValue];
    for (int i = 0; i < swigValues.length; i++)
      if (swigValues[i].swigValue == swigValue)
        return swigValues[i];
    throw new IllegalArgumentException("No enum " + TypeFlags.class + " with value " + swigValue);
  }

  private TypeFlags(String swigName) {
    this.swigName = swigName;
    this.swigValue = swigNext++;
  }

  private TypeFlags(String swigName, int swigValue) {
    this.swigName = swigName;
    this.swigValue = swigValue;
    swigNext = swigValue+1;
  }

  private TypeFlags(String swigName, TypeFlags swigEnum) {
    this.swigName = swigName;
    this.swigValue = swigEnum.swigValue;
    swigNext = this.swigValue+1;
  }

  private static TypeFlags[] swigValues = { eTypeHasChildren, eTypeHasValue, eTypeIsArray, eTypeIsBlock, eTypeIsBuiltIn, eTypeIsClass, eTypeIsCPlusPlus, eTypeIsEnumeration, eTypeIsFuncPrototype, eTypeIsMember, eTypeIsObjC, eTypeIsPointer, eTypeIsReference, eTypeIsStructUnion, eTypeIsTemplate, eTypeIsTypedef, eTypeIsVector, eTypeIsScalar, eTypeIsInteger, eTypeIsFloat, eTypeIsComplex, eTypeIsSigned, eTypeInstanceIsPointer };
  private static int swigNext = 0;
  private final int swigValue;
  private final String swigName;
}

