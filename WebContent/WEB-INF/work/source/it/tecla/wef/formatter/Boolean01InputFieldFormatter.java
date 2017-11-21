package it.tecla.wef.formatter;

import java.util.Collections;
import java.util.List;

import com.bowstreet.methods.BaseInputFieldFormatter;

public class Boolean01InputFieldFormatter extends BaseInputFieldFormatter {

	@Override
	public String format(String value, String format) {
		if (value != null && value.trim().equals("1")) {
			return "1";
		}
		return "0";
	}
	
	@Override
	public String translate(String value, String format) {
		this.setTranslateSuccessFlag(true);
		if (value != null && value.trim().equals("1")) {
			return "1";
		}
		return "0";
	}
	
	@Override
	public boolean validate(String value, String expression) {
		return value != null && (value.equals("0") || value.equals("1"));
	}
	
	@Override
	public List<String> getFormatExpressionList() {
		return Collections.singletonList("DEFAULT");
	}
	
	@Override
	public List<String> getTranslateExpressionList() {
		return Collections.singletonList("DEFAULT");
	}
	
	@Override
	public List<String> getValidateExpressionList() {
		return Collections.singletonList("DEFAULT");
	}
	
}
