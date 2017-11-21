package it.tecla.wef.builders;

import com.bowstreet.builders.webapp.TextInputBuilder;
import com.bowstreet.util.IXml;
import com.bowstreet.webapp.Page;

public class GenericInputBuilder extends TextInputBuilder {

	@Override
	protected void handleControl(Page page, IXml element) {
		super.handleControl(page, element);
		element.setAttribute("type", this.builderInputs.getString("Type", "text"));
	}

	@Override
	public Object newInstance() {
		return new GenericInputBuilder();
	}
}
